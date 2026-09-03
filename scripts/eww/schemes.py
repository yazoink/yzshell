#!/usr/bin/env python

import json
import subprocess
from os import listdir, path, environ
from sys import argv, exit

CACHE_FILE = path.join(environ["YZSHELL_CACHE_DIR"], "schemes.json")


def update_eww(arrs):
    for a in arrs:
        empty = "true"
        if len(arrs[a]) > 0:
            empty = "false"
        subprocess.run(
            f"""
            eww update {a}_colourschemes="{json.dumps(arrs[a]).replace("\"", "\\\"")}"
            eww update no_{a}_schemes_found={empty}
            """,
            shell=True,
        )


def get_all(refresh=False):
    def sort_schemes(schemes):
        return sorted(schemes, key=lambda d: d["scheme"].lower())

    r = {"dark": [], "light": []}

    if path.isfile(CACHE_FILE) and not refresh:
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass

    directory = environ["YZSHELL_COLOURS_DIR"]
    files_list = listdir(directory)
    for n in files_list:
        j = ""
        with open(f"{directory}/{n}", "r") as f:
            j = f.read()
        j = json.loads(j)
        j["id"] = n.replace(".json", "")
        if "window_buttons" not in j:
            j["window_buttons"] = ["red", "yellow", "green"]
        if "accent" not in j:
            j["accent"] = "blue"
        r[j["polarity"]].append(j)
    for a in r:
        r[a] = sort_schemes(r[a])
    return r


def filter_arr(qry, a):
    r = []
    for sch in a:
        name = sch["scheme"].lower()
        if qry in sch["id"] or qry in name:
            if sch["id"].startswith(qry) or name.startswith(qry):
                r.insert(0, sch)
            else:
                r.append(sch)
    return r


arrs = get_all()

if len(argv) < 2:
    subprocess.run("eww update scheme_query=''", shell=True)
    update_eww(get_all(refresh=True))
    exit(0)

if argv[1].strip() == "":
    update_eww(get_all())
    exit(0)

qry = argv[1].lower()
print("qry: " + qry)
for a in arrs:
    arrs[a] = filter_arr(qry, arrs[a])
update_eww(arrs)
