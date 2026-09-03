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


def update_thumbs(refresh=False, directory=None):
    cache_dir = environ["YZSHELL_WALLPAPER_CACHE_DIR"]

    def make_thumb(f):
        with Image.open(path.join(directory, f)) as i:
            MAX_SIZE = (150, 150)
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


if __name__ == "__main__":
    lockfile = environ["YZSHELL_WALLPAPER_LOCKFILE"]

    if path.isfile(lockfile) == True:
        exit(1)
    with open(lockfile, "w") as f:
        f.write("")

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", default=None)
    parser.add_argument("-c", "--columns", default=3)
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
        eww update wallpapers_loading=true
        eww update wallpapers="[]"
        """,
        shell=True,
    )

    update_thumbs(directory=directory, refresh=args.refresh)

    image_files = get_image_files(directory)
    wallpaper_data = get_wallpaper_data(image_files, args.columns)

    subprocess.run(
        f"""
        eww update wallpapers_loading=false
        eww update wallpapers=\'{json.dumps(wallpaper_data)}\'
        """,
        shell=True,
    )
    #print(json.dumps(wallpaper_data))
    remove(lockfile)