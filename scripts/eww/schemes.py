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


def get_current_page_index():
    try:
        r = int(subprocess.run(
            ["eww", "get", "colourschemes_page"],
            text=True,
            capture_output=True
        ).stdout.strip())
        return r
    except:
        return 0


def get_page(index, a):
    sch_num = len(a)
    start_index = MAX_PER_PAGE * index
    end_index = start_index + MAX_PER_PAGE
    #print("sch_num: " + str(sch_num))
    #print("start_index: " + str(start_index))
    #print("end_index: " + str(end_index))
    if end_index >= sch_num:
        end_index = sch_num
    return a[start_index:end_index]


def get_polarity():
    r = subprocess.run(
        ["eww", "get", "schemes_selected"],
        capture_output=True,
        text=True
    ).stdout.strip()
    if r == "1":
        return "light"
    else:
        return "dark"


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--page", default=None)
    parser.add_argument("-q", "--query", default="")
    parser.add_argument("-p", "--polarity", default=None)
    parser.add_argument("-r", "--refresh", action="store_true", default=False)
    args = parser.parse_args(argv[1:])

    qry = args.query.strip()
    polarity = args.polarity
    schemes = None
    arrs = None

    subprocess.run(
        f"""
        eww update schemes_loading=true
        eww update colourschemes="[]"
        """,
        shell=True
    )

    arrs = get_all(refresh=args.refresh)

    # get schemes
    if qry != "":
        schemes = filter_arr(args.query, arrs[polarity])
    else:
        schemes = arrs[polarity]

    current_page = get_current_page_index()
    if args.page != None:
        sch_num = len(schemes)
        max_pages = ceil(sch_num / MAX_PER_PAGE)
        target_page = args.page
        if args.page == "next":
            target_page = current_page + 1
            if target_page >= max_pages:
                target_page = 0
        elif args.page == "prev":
            target_page = current_page - 1
            if target_page < 0:
                target_page = max_pages - 1
        else:
            target_page = int(target_page)
            if target_page >= max_pages:
                target_page = max_pages - 1
            elif target_page < 0:
                target_page = 0
        current_page = target_page
                
    if len(schemes) > 0:
        schemes = get_page(current_page, schemes)
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

    #print(json.dumps(arrs[polarity], indent=4))
    subprocess.run(
        f"""
        eww update colourschemes="{json.dumps(schemes).replace("\"", "\\\"")}"
        eww update colourschemes_page='{str(current_page)}'
        eww update schemes_loading=false
        """,
        shell=True
    )