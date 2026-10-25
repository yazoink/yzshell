#!/usr/bin/env python

import argparse
import json
import subprocess
from math import ceil
from os import listdir, makedirs, path, remove, environ
from shutil import rmtree
from sys import argv, exit
from sys import path as sys_path
from threading import Thread

from PIL import Image

sys_path.append(environ["YZSHELL_PYTHON_LIB_DIR"])
from configutils import get_config
from miscutils import get_full_path

MAX_PER_PAGE = 4 # max items per page


def get_image_files(directory):
    files = listdir(directory)
    image_files = []
    for f in files:
        if f.endswith((".jpg", ".png", ".jpeg")):
            image_files.append(f)
    return sorted(image_files)


def get_wallpaper_data(image_files, cols):
    a = []
    l = len(image_files)
    if l > 0:
        rows = ceil(l / cols)

        i = 0
        for _ in range(0, rows):
            r = []
            for _ in range(0, cols):
                if i < l:
                    r.append(image_files[i])
                    i += 1
                else:
                    break
            a.append(r)
    return a


def get_page(wallpapers, wp_num, index):
    start_index = MAX_PER_PAGE * index
    end_index = start_index + MAX_PER_PAGE
    if end_index >= wp_num:
        end_index = wp_num
    return wallpapers[start_index:end_index]


def update_thumbs(refresh=False, directory=None):
    cache_dir = environ["YZSHELL_WALLPAPER_CACHE_DIR"]

    def make_thumb(f):
        with Image.open(path.join(directory, f)) as i:
            MAX_SIZE = (156, 156)
            i.thumbnail(MAX_SIZE)
            i.save(path.join(cache_dir, f))

    if path.exists(cache_dir) == True:
        if refresh == True:
            rmtree(cache_dir)
            makedirs(cache_dir)
    else:
        makedirs(cache_dir)

    files = listdir(directory)
    threads = []
    img_num = 0
    for f in files:
        l = f.lower()
        if l.endswith((".jpg", ".png", ".jpeg")):
            img_num += 1
            if path.exists(path.join(cache_dir, f)) == False:
                threads.append(Thread(target=make_thumb, args=(f,)))
    if img_num < 1:
        return False
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return True


def get_current_page():
    return int(subprocess.run(
        ["eww", "get", "wallpapers_page"],
        text=True,
        capture_output=True
    ).stdout.strip())


if __name__ == "__main__":
    lockfile = environ["YZSHELL_WALLPAPER_LOCKFILE"]

    if path.isfile(lockfile) == True:
        exit(1)
    with open(lockfile, "w") as f:
        f.write("")

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", default=None)
    parser.add_argument("-c", "--columns", default=3)
    parser.add_argument("-p", "--page", default=None)
    parser.add_argument("-r", "--refresh", action="store_true", default=False)
    args = parser.parse_args(argv[1:])

    default_dir = get_config()["wallpaper_dir"]
    directory = args.directory
    if directory is not None:
        directory = get_full_path(directory)
        if path.isdir(directory) == False:
            directory = default_dir
    else:
        directory = default_dir

    subprocess.run(
        f"""
        eww update wallpaper_dir='{directory}'
        eww update wallpapers="[]"
        eww update wallpapers_loading=true
        """,
        shell=True,
    )

    if args.refresh == True:
        subprocess.run(
            "eww update wallpapers_page='0'",
            shell=True,
        )

    update_thumbs(directory=directory, refresh=args.refresh)
    image_files = get_image_files(directory)
    wallpaper_data = get_wallpaper_data(image_files, args.columns)

    page = 0
    wp_num = len(wallpaper_data)
    page_num = ceil(wp_num / MAX_PER_PAGE)

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

    #print(json.dumps(wallpaper_data, indent=4))
    wallpaper_data = get_page(wallpaper_data, wp_num, page)

    subprocess.run(
        f"""
        eww update wallpapers_page="{page}"
        eww update wallpapers=\'{json.dumps(wallpaper_data)}\'
        eww update wallpapers_loading=false
        """,
        shell=True,
    )
    #print(json.dumps(wallpaper_data, indent=4))
    remove(lockfile)