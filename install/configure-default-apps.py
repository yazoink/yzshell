#!/usr/bin/env python

from os import path
from os import environ
import json
import subprocess
from utils import install_pkgs, choose, confirm, get_input, update_config


apps = None
with open(path.join(environ["REPO_DIR"], "misc/apps.json"), "r") as f:
    apps = json.load(f)

for category in apps:
    title = apps[category]["title"]
    cmd = None
    a = apps[category]["apps"]
    a["other"] = {}
    c = choose(title, a)
    if c == "other":
        while True:
            cmd = get_input(f"Enter {title} command...")
            if confirm(f"Set {title} to '{cmd}'?"):
                break
    else:
        cmd = c
        if "deps" in apps[category]["apps"][c]:
            install_pkgs(apps[category]["apps"][c]["deps"])
        if "aur_deps" in apps[category]["apps"][c]:
            install_pkgs(apps[category]["apps"][c]["aur_deps"], aur=True)
    update_config(category, cmd)