#!/usr/bin/env python

from os import path, environ, makedirs
import json
from gi.repository import Gio
import subprocess
from sys import argv
from sys import path as sys_path

sys_path.append(environ["YZSHELL_PYTHON_LIB_DIR"])
from configutils import get_config

REPLACE = {
    "vesktop": "vesktop --enable-features=UseOzonePlatform --ozone-platform=wayland"
}


def update_app_cache(cache_file, all_apps):
    d = path.dirname(cache_file)
    if not path.exists(d):
        makedirs(d)
    with open(cache_file, "w") as f:
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

def get_cached_apps(cache_file, refresh=False):
    if path.exists(cache_file) and not refresh:
        with open(cache_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    all_apps = []
    terminal = get_config()["terminal"]
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
    update_app_cache(cache_file, all_apps)
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


def update_eww(var, val, string=False):
    if string == True:
        val=f"\"{val.replace("\"", "\\\"")}\""
    #print(f"eww update {var}={val}")
    subprocess.run(
        f"eww update {var}={val}",
        shell=True
    )


if __name__ == "__main__":
    argc = len(argv)
    query = ""
    if argc > 1:
        query = argv[1]
    cache_file = path.join(environ["YZSHELL_CACHE_DIR"], "apps.json")
    if query.strip() != "":
        update_eww("search_selected", 0)
        apps = filter_top(filter_entries(get_cached_apps(cache_file), query), 10)
        update_eww("search_results", json.dumps(apps), True)
        #print(json.dumps(apps))
    else:
        update_eww("search_selected", -1)
        apps = get_cached_apps(cache_file, refresh=True)
        update_eww("search_results", json.dumps(apps), True)
        #print(json.dumps(apps))