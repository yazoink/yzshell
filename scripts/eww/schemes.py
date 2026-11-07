#!/usr/bin/env python

import json
import subprocess
from os import listdir, path, environ
from sys import argv, exit
from math import ceil
from argparse import ArgumentParser
from random import randint

CACHE_FILE = path.join(environ["YZSHELL_CACHE_DIR"], "schemes.json")
MAX_PER_PAGE = 8 # max items per page


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
    qry = qry.lower()
    for sch in a:
        name = sch["scheme"].lower()
        if qry in sch["id"] or qry in name:
            #print(name)
            if sch["id"].startswith(qry) or name.startswith(qry):
                r.insert(0, sch)
            else:
                r.append(sch)
    return r


def get_target_page_index(arg):
    page = None
    sch_num = len(schemes)
    max_pages = ceil(sch_num / MAX_PER_PAGE)

    try:
        page = int(arg)
    except:
        page = int(subprocess.run(
            ["eww", "get", "colourschemes_page"],
            text=True,
            capture_output=True
        ).stdout.strip())

    if arg == "next":
        page += 1
        if page >= max_pages:
            page = 0
    elif arg == "prev":
        page -= 1
        if page < 0:
            page = max_pages - 1
    else:
        if page >= max_pages:
            page = max_pages - 1
        elif page < 0:
            page = 0
    return page


def get_page(index, schemes):
    sch_num = len(schemes)
    start_index = MAX_PER_PAGE * index
    end_index = start_index + MAX_PER_PAGE
    #print("sch_num: " + str(sch_num))
    #print("start_index: " + str(start_index))
    #print("end_index: " + str(end_index))
    if end_index >= sch_num:
        end_index = sch_num
    return schemes[start_index:end_index]


def set_offsets(schemes):
    offset_x = 0
    offset_direction = "r"
    offset_inc = 32
    offset_max_l = -64
    offset_max_r = 64
    for i in range(0, len(schemes)):
        schemes[i]["offset-x"] = str(offset_x)
        schemes[i]["offset-y"] = str(randint(-48, 8))

        if offset_direction == "l":
            if offset_x == offset_max_l:
                offset_direction = "r"
                offset_x += offset_inc
            else:
                offset_x -= offset_inc
        elif offset_direction == "r":
            if offset_x == offset_max_r:
                offset_direction = "l"
                offset_x -= offset_inc
            else:
                offset_x += offset_inc
    schemes[0]["offset-y"] = str(randint(0, 8))
    return schemes


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--page", default=None)
    parser.add_argument("-q", "--query", default="")
    parser.add_argument("-p", "--polarity", default=None)
    parser.add_argument("-r", "--refresh", action="store_true", default=False)
    args = parser.parse_args(argv[1:])

    qry = args.query.strip() # query
    arrs = None # all schemes
    schemes = None # schemes array to pass to eww
    page = None # index of target page

    subprocess.run(
        f"""
        eww update schemes_loading=true
        eww update colourschemes="[]"
        """,
        shell=True
    )

    # get schemes
    arrs = get_all(refresh=args.refresh)
    if qry != "":
        schemes = filter_arr(args.query, arrs[args.polarity])
    else:
        schemes = arrs[args.polarity]

    # get target page index
    page = get_target_page_index(args.page)
                
    # get page and set offsets
    if len(schemes) > 0:
        schemes = set_offsets(get_page(page, schemes))

    #print(json.dumps(arrs[args.polarity], indent=4))
    subprocess.run(
        f"""
        eww update colourschemes="{json.dumps(schemes).replace("\"", "\\\"")}"
        eww update colourschemes_page='{str(page)}'
        eww update schemes_loading=false
        """,
        shell=True
    )