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


def update_eww(a, polarity):
    empty = "true"
    if len(a) > 0:
        empty = "false"
    subprocess.run(
        f"""
        eww update {polarity}_colourschemes="{json.dumps(a).replace("\"", "\\\"")}"
        eww update no_schemes_found={empty}
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
    qry = qry.lower()
    for sch in a:
        name = sch["scheme"].lower()
        if qry in sch["id"] or qry in name:
            print(name)
            if sch["id"].startswith(qry) or name.startswith(qry):
                r.insert(0, sch)
            else:
                r.append(sch)
    return r


def get_current_page_index(polarity):
    cmd = ["eww", "get"]
    if polarity == "dark":
        cmd.append("dark_colourschemes_page")
    else:
        cmd.append("light_colourschemes_page")
    try:
        r = int(subprocess.run(
            cmd,
            text=True,
            capture_output=True
        ).stdout.strip())
        return r
    except:
        return 0


def get_page(index, a, polarity):
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
    if r == 1:
        return "light"
    else:
        return "dark"


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--page", default=None)
    parser.add_argument("-q", "--query", default="")
    parser.add_argument("-p", "--polarity", default=None)
    args = parser.parse_args(argv[1:])

    qry = args.query.strip()
    polarity = None
    if args.polarity != None:
        if args.polarity in ["dark", "light"]:
            polarity = args.polarity
        else:
            polarity = get_polarity()
    else:
        polarity = get_polarity()

    refresh = False
    if qry == "":
        refresh = True

    arrs = get_all(refresh=refresh)

    if qry == "":
        subprocess.run("eww update scheme_query=''", shell=True)
    else:
        arrs[polarity] = filter_arr(args.query, arrs[polarity])

    if args.page != None:
        current_page = get_current_page_index(polarity)
        sch_num = len(arrs[polarity])
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
        subprocess.run(
            f"eww update {polarity}_colourschemes_page='{str(target_page)}'",
            shell=True
        )
                
    if len(arrs[polarity]) > 0:
        p = get_current_page_index(polarity)
        arrs[polarity] = get_page(p, arrs[polarity], polarity)
        offset_x = 0
        offset_direction = "r"
        offset_inc = 32
        offset_max_l = -64
        offset_max_r = 64
        for i in range(0, len(arrs[polarity])):
            arrs[polarity][i]["offset-x"] = str(offset_x)
            arrs[polarity][i]["offset-y"] = str(randint(-32, 8))
            #arrs[a][i]["offset-y"] = "-32"

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
        arrs[polarity][0]["offset-y"] = str(randint(0, 8))

    #print(json.dumps(arrs[polarity], indent=4))
    #print(polarity)
    update_eww(arrs[polarity], polarity)