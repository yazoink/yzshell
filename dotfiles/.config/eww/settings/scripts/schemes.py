#!/usr/bin/env python

import subprocess
import json
from sys import argv, exit
from os import path, listdir

CACHE_FILE = "/tmp/all_colourschemes.json"

def update_eww(arrs):
    for a in arrs:
        subprocess.run(
            f"eww update {a}_colourschemes=\"{json.dumps(arrs[a]).replace("\"", "\\\"")}\"",
            shell=True
        )

def get_all(refresh=False):
    def sort_schemes(schemes):
        return sorted(schemes, key=lambda d: d["scheme"])

    r = {"dark": [], "light": []}

    if path.isfile(CACHE_FILE) and not refresh:
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass

    directory = path.expanduser("~/.local/share/yzshell/colourschemes")
    files_list = listdir(directory)
    for n in files_list:
        j = ""
        with open(f"{directory}/{n}", "r") as f:
            j = f.read()
        j = json.loads(j)
        j["id"] = n.replace(".json", "")
        r[j["polarity"]].append(j)
    for a in r:
        r[a] = sort_schemes(r[a])
    return r

def filter_arr(qry, a):
    r = []
    for sch in a:
        name = sch["scheme"].lower()
        if qry in sch["id"] or qry in name:
            if qry.startswith(sch["id"]) or qry.startswith(name):
                r.insert(0, sch)
            else:
                r.append(sch)
    return r

arrs = get_all()

if len(argv) < 2:
    print("no qry, updating")
    subprocess.run("eww update scheme_query=''", shell=True)
    update_eww(get_all(refresh=True))
    exit(0)

if argv[1].strip() == "":
    print("no qry, not updating")
    update_eww(get_all())
    exit(0)

qry = argv[1].lower()
print("qry: " + qry)
for a in arrs:
    arrs[a] = filter_arr(qry, arrs[a])
update_eww(arrs)