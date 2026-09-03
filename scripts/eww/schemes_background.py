#!/usr/bin/env python

import subprocess
from os import makedirs, path, environ
from PIL import Image
from sys import path as sys_path

sys_path.append(environ["YZSHELL_PYTHON_LIB_DIR"])
from configutils import get_config


def main():
    config = get_config()
    cache_dir = environ["YZSHELL_WALLPAPER_CACHE_DIR"]
    wp_dir = config["wallpaper_dir"]
    wp_img = config["wallpaper_image"]
    wp_path = path.join(wp_dir, wp_img)
    target_path = path.join(cache_dir, f"cropped_{wp_img}")
    target_w = 530
    target_h = 300

    if not path.exists(cache_dir):
        makedirs(cache_dir)

    if not path.isfile(target_path):
        with Image.open(wp_path) as im:
            w, h =  im.size
            left = 0
            upper = 0
            right = w
            lower = h
            if w > target_w:
                left = (w / 2) - (target_w / 2)
                right = (w / 2) + (target_w / 2)
            if h > target_h:
                upper = (h / 2) - (target_h / 2)
                lower = (h / 2) + (target_h / 2)
            im.crop((
                left, 
                upper, 
                right, 
                lower
            )).save(target_path)
    
    subprocess.Popen(
        f"eww update colourschemes_bg_image='{target_path}'",
        shell=True
    )

main()
