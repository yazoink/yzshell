#!/usr/bin/env python

import json
from os import path, environ
from sys import argv, exit
from gi.repository import Gio
import re
import subprocess


CACHE_FILE="/tmp/yzshell_search_cache.json"


def get_results(query = ""):
    all_apps = []
    # load cached app array
    if path.isfile(CACHE_FILE) == False:
        update_cache()
        
    with open(CACHE_FILE, "r") as f:
        j = f.read()
        all_apps = json.loads(j)

    # if empty search, return all
    if query == "":
        return json.dumps(all_apps)
    
    # get results array    
    results = []
    for a in all_apps:
        n = a["name"].lower()
        d = a["desc"].lower()
        if query in n or query in d:
            if n.startswith(query):
                results.insert(0, a)
            else:
                results.append(a)
    
    # re-index
    for i in range(0, len(results)):
        results[i]["index"] = i
    #print(results)
    return json.dumps(results)

        
def update_cache():
    all_apps = []
    app_info = Gio.AppInfo.get_all()
    i = 0
    for app in app_info:
        if app.should_show() == False:
            continue
        cmd = ""
        if app.get_boolean("Terminal"):
            cmd = f"{environ["TERM"]} -e "
        cmd += app.get_commandline()
        cmd = re.sub("%[a-zA-Z]", "", cmd)
        cmd = re.sub(" -- $", "", cmd)
        icon = "question"
        icon_obj = app.get_icon()
        if icon_obj != None:
            icon = Gio.Icon.to_string(icon_obj)
        desc = app.get_description()
        if desc == None:
            desc = "No description"
        all_apps.append(
            {
                "name": app.get_display_name(),
                "desc": desc,
                "cmd": cmd, # launch command
                "icon": icon,
                "bin": app.get_executable(), # base binary file
                "index": i,
            }
        )
        i += 1
    j = json.dumps(all_apps)
    with open(CACHE_FILE, "w") as f:
        f.write(j)
            
            
def main():
    argc = len(argv)
    if argc < 2:
        print("Error: not enough args")
        exit(1)
    if argv[1] == "get_results":
        query = ""
        selected = -1
        if argc > 2:
            query = argv[2]
            if query != "":
                selected = 0
        results = get_results(query)
        subprocess.run(f"eww update search_selected={str(selected)}", shell=True)
        subprocess.run(f"eww update search_results='{results}'", shell=True)
        #print(results)
    elif argv[1] == "update_cache":
        update_cache()
        
        
main()
           
