#!/usr/bin/env python

import argparse
import json
import subprocess
from math import floor
from os import listdir, makedirs, path
from shutil import rmtree
from sys import argv, exit
from threading import Thread

from PIL import Image


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

    if path.isdir(directory) == False:
        subprocess.run(
            f'''
            eww update wallpaper_dir="$(yzconf get wallpaper_dir)"
            ''',
            shell=True
        )
        exit(1)

    subprocess.run(
        f'''
        eww update wallpapers_loading=true
        eww update wallpapers="[]"
        ''',
        shell=True
    )

    # update thumbs
    update_thumbs(directory=directory, refresh=args.refresh)

    files = listdir(directory)
    image_files = []
    for f in files:
        if f.endswith(('.jpg', '.png', '.jpeg')):
            image_files.append(f)
    if len(image_files) > 1:
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
        f'''
        eww update wallpapers_loading=false
        eww update wallpapers=\'{json.dumps(available_wallpapers)}\'
        ''',
        shell=True
    )
