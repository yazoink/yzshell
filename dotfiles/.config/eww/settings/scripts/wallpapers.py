#!/usr/bin/env python

import subprocess
import json
from os import path, listdir, makedirs
from shutil import rmtree
from math import floor
from threading import Thread
from PIL import Image
from sys import exit, argv
import argparse


def get_default_dir():
    return subprocess.run(
        "yzconf get wallpaper_dir",
        shell=True,
        text=True,
        capture_output=True
    ).stdout.strip()


def get_dir(arg):
    directory = None
    if arg is not None:
        directory = path.expanduser(arg)
        if path.exists(directory) == False:
            directory = path.expanduser(get_default_dir())
    else:
        directory = path.expanduser(get_default_dir())
    return directory


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
        if l.endswith(('.jpg', '.png', '.jpeg')):
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", default=None)
    parser.add_argument("-r", "--refresh", action='store_true', default=False)
    args = parser.parse_args(argv[1:])

    directory = get_dir(args.directory)
    columns = 3
    available_wallpapers = []
    cols = 0
    rows = 0

    subprocess.run(
        '''eww update wallpapers="[]"
        eww update dir_has_wallpapers=true''',
        shell=True
    )

    # update thumbs
    if not update_thumbs(directory=directory, refresh=args.refresh):
        subprocess.run(
            '''eww update dir_has_wallpapers=false
            eww update wallpapers="[]"''',
            shell=True
        )
        exit(1)

    subprocess.run(
        f"eww update wallpaper_dir='{directory}'",
        shell=True
    )
    files = listdir(directory)
    image_files = []
    for f in files:
        if f.endswith(('.jpg', '.png', '.jpeg')):
            image_files.append(f)
    if len(image_files) < 3:
        rows = 1
    else:
        rows = floor(len(files) / 3)

    i = 0
    for row in range(0, rows):
        cols = 3
        available_wallpapers.append([])
        for _ in range(0, cols):
            if i < len(image_files):
                available_wallpapers[row].append(image_files[i])
                i += 1
    subprocess.run(
        f"eww update wallpapers='{json.dumps(available_wallpapers)}'",
        shell=True
    )