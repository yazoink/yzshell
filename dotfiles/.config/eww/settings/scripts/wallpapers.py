#!/usr/bin/env python

import argparse
import json
import subprocess
from math import ceil
from os import listdir, makedirs, path, remove
from shutil import rmtree
from sys import argv, exit
from threading import Thread

from PIL import Image


def get_default_dir():
    return subprocess.run(
        "yzconf get wallpaper_dir", shell=True, text=True, capture_output=True
    ).stdout.strip()


def get_dir(arg):
    directory = None
    if arg is not None:
        directory = path.expanduser(arg)
    else:
        directory = path.expanduser(get_default_dir())
    return directory


def get_image_files(directory):
    files = listdir(directory)
    image_files = []
    for f in files:
        if f.endswith((".jpg", ".png", ".jpeg")):
            image_files.append(f)
    return sorted(image_files)


def get_wallpaper_data(image_files, cols):
    a = []
    if len(image_files) > 0:
        rows = ceil(len(image_files) / cols)

        i = 0
        for _ in range(0, rows):
            r = []
            for _ in range(0, cols):
                r.append(image_files[i])
                i += 1
            a.append(r)
    return a


def update_thumbs(refresh=False, directory=None):
    cache_dir = "/tmp/wallpaper_cache"

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
    lockfile = "/tmp/wp_settings.lock"

    if path.isfile(lockfile) == True:
        exit(1)
    with open(lockfile, "w") as f:
        f.write("")

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", default=None)
    parser.add_argument("-c", "--columns", default=3)
    parser.add_argument("-r", "--refresh", action="store_true", default=False)
    args = parser.parse_args(argv[1:])

    directory = get_dir(args.directory)

    # invalid dir
    if path.isdir(directory) == False:
        directory = subprocess.run(
            ["yzconf", "get", "wallpaper_dir"], text=True, capture_output=True
        ).stdout.strip()
        subprocess.run(
            f"eww update wallpaper_dir='{directory}'",
            shell=True,
        )
        remove(lockfile)
        exit(1)

    # valid dir
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
    remove(lockfile)
