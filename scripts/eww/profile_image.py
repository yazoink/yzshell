#!/usr/bin/env python

import subprocess
from os import environ, path

if __name__ == "__main__":
    filetypes = [".png", ".jpg", ".jpeg"]
    subprocess.run(["yzwidgets", "close", "all"])
    selected = subprocess.run(
        [path.join(environ["YZSHELL_SCRIPT_DIR"], "filepicker.py")],
        text=True,
        capture_output=True
    ).stdout.strip()
    valid = False
    for f in filetypes:
        if selected.endswith(f):
            valid = True
            break
    if valid == True:
        subprocess.run(
            f"""
            yzconf set profile_image "{selected}"
            eww update profile_image="{selected}"
            """,
            shell=True
        )
    else:
        subprocess.run(
            "notify-send 'Could not change profile image!' 'Invalid file'",
            shell=True
        )
    subprocess.run(["yzwidgets", "open", "settings"])