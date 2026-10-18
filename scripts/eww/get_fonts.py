#!/usr/bin/env python

import subprocess
import json
from sys import argv
from os import environ, path, makedirs
from argparse import ArgumentParser
from math import ceil

CACHE_FILE=path.join(environ["YZSHELL_CACHE_DIR"], "fonts.json")
MAX_PER_PAGE = 16 # max items per page


def remove_trailing(fonts):
    r = []
    for f in fonts:
        s, _, _ = f.partition(",")
        if s != "" and s not in r:
            r.append(s)
    return r


def get_all():
    fonts = None
    if path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                fonts = json.load(f)
            fonts = remove_trailing(fonts)
            return fonts
        except:
            pass
    fonts = subprocess.run(
        "fc-list : family",
        shell=True,
        text=True,
        capture_output=True
    ).stdout.split("\n")
    fonts = remove_trailing(fonts)
    if path.exists(environ["YZSHELL_CACHE_DIR"]) == False:
        makedirs(environ["YZSHELL_CACHE_DIR"])
    with open(CACHE_FILE, "w") as f:
        json.dump(sorted(fonts), f)
    return fonts


def filter_fonts(fonts, qry):
    print(qry)
    r = []
    for f in fonts:
        g = f.lower()
        if qry in g:
            print(qry + " in " + g)
            if qry.startswith(g):
                r.insert(0, f)
                print("inserting: " + f)
            else:
                r.append(f)
                print("appending: " + f)
    return r


def get_page(index, font_num, fonts):
    start_index = MAX_PER_PAGE * index
    end_index = start_index + MAX_PER_PAGE
    print("start_index: " + str(start_index))
    print("end_index: " + str(end_index))
    print("font_num: " + str(font_num))
    if end_index >= font_num:
        end_index = font_num
    return fonts[start_index:end_index]


def get_current_page():
    return int(subprocess.run(
        ["eww", "get", "fonts_page"],
        text=True,
        capture_output=True
    ).stdout.strip())


if __name__ == "__main__":
    fonts = get_all()
    
    parser = ArgumentParser()
    parser.add_argument("-i", "--page", default=None)
    parser.add_argument("-q", "--query", default=None)
    args = parser.parse_args(argv[1:])

    if args.query == None:
        qry = subprocess.run(
            ["eww", "get", "fonts_query"],
            text=True,
            capture_output=True
        ).stdout.strip().lower()
    else:
        qry = args.query.lower()
    if qry != "":
        fonts = filter_fonts(fonts, qry)

    page = 0
    font_num = len(fonts)
    page_num = ceil(font_num / MAX_PER_PAGE)

    if args.page != None:
        if args.page in ["next", "prev"]:
            current_page = get_current_page()
            page = current_page
            if args.page == "next":
                if page + 1 >= page_num:
                    page = 0
                else:
                    page += 1
            else:
                if page - 1 < 0:
                    page = page_num - 1
                else:
                    page -= 1
        else:
            page = int(args.page)
            if page >= page_num:
                page = page_num - 1
            elif page <= page_num:
                page = 0
    else:
        page = get_current_page()

    fonts = get_page(page, font_num, fonts)

    subprocess.run(
        f"""
        eww update fonts_page='{str(page)}'
        eww update fonts='{json.dumps(fonts).replace("'", "\\'")}'
        """,
        shell=True
    )
    print(json.dumps(fonts))