#!/usr/bin/env python

from os import path
import json
from gi.repository import Gio
from subprocess import run
from sys import argv

APP_CACHE_FILE=path.expanduser("~/.cache/yzshell/apps.json")
INDEX_CACHE_FILE=path.expanduser("~/.cache/yzshell/apps_index.json")
TERM_CACHE_FILE=path.expanduser("~/.cache/yzshell/apps_term")
REPLACE = {
    "vesktop": "vesktop --enable-features=UseOzonePlatform --ozone-platform=wayland"
}


def get_terminal():
    if path.exists(TERM_CACHE_FILE):
        with open(TERM_CACHE_FILE, "r") as f:
            return f.read.strip()
    return run(
        ["yzconf", "get", "terminal"],
        capture_output=True,
        text=True
    ).stdout.strip()


def update_app_cache(all_apps):
    with open(APP_CACHE_FILE, "w") as f:
        json.dump(all_apps, f)


def get_desktop_entries(app_info, index, terminal):
    # desc
    app_name = app_info.get_name()
    app_desc = app_info.get_description()
    if app_desc == None:
        app_desc = "No description"
    # bin
    app_binary = app_info.get_executable()
    # cmd
    app_cmd = ""
    if app_info.get_boolean("Terminal"):
        app_cmd = f"{terminal} -e "
    app_cmd += app_binary
    #icon
    app_icon = "unknown"
    icon_obj = app_info.get_icon()
    if icon_obj != None:
        app_icon = Gio.Icon.to_string(icon_obj)
    return {
        "name": app_name.title(),
        "desc": app_desc,
        "cmd": app_cmd, # launch command
        "icon": app_icon,
        "bin": 
            REPLACE[app_binary] 
            if app_binary in REPLACE 
            else app_binary, # base binary file
        "index": index,
    }

def get_cached_apps(refresh=False):
    if path.exists(APP_CACHE_FILE) and not refresh:
        with open(APP_CACHE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    all_apps = []
    terminal = get_terminal()
    app_info = Gio.AppInfo
    i = 0
    for app_info in app_info.get_all():
        if not app_info.should_show():
            continue
        all_apps.append(get_desktop_entries(app_info, i, terminal))
        i += 1
    #all_apps = sorted(all_apps, key=lambda x: x["name"])
    #i = 0
    #for a in all_apps:
    #    a["index"] = i
    #    i += 1
    update_app_cache(all_apps)
    return all_apps


def filter_entries(all_apps, query):
    query = query.lower()
    filtered_data = []
    for app in all_apps:
        app_name = app["name"].lower()
        app_binary = app["bin"].lower()
        app_desc = app["desc"].lower()
        if app_name.startswith(query) or app_binary.startswith(query):
            filtered_data.insert(0, app)
        elif query in app_desc or query in app_name or query in app_binary:
            filtered_data.append(app)
    i = 0
    for app in filtered_data:
        app["index"] = i
        i += 1
    return filtered_data


def filter_top(apps, n): 
    apps = apps[:n]
    return apps


def update_eww(var, val):
    run(
        ["eww", "update", f"{var}={val}"]
    )


if __name__ == "__main__":
    argc = len(argv)
    query = ""
    if argc > 1:
        query = argv[1]
    if query.strip() != "":
        update_eww("search_selected", 0)
        apps = filter_top(filter_entries(get_cached_apps(), query), 10)
        update_eww("search_results", json.dumps(apps))
        #print(json.dumps(apps))
    else:
        update_eww("search_selected", -1)
        apps = get_cached_apps(refresh=True)
        update_eww("search_results", json.dumps(apps))
        #print(json.dumps(apps))