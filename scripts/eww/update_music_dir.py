#!/usr/bin/env python

import chevron
from os import environ, path
from sys import argv, exit
from sys import path as sys_path

sys_path.append(environ["YZSHELL_PYTHON_LIB_DIR"])
from configutils import get_config

if __name__ == "__main__":
    if len(argv) < 2:
        print("Error: no dir specified")
        exit(1)
    config = get_config()
    dir = path.expanduser(argv[1])
    templates = {
        "mpd.conf.mustache": ".config/mpd/mpd.conf",
        "ncmpcpp.mustache": ".config/ncmpcpp/config"
    }
    data = {"music_dir": dir}
    for t in templates:
        s = None
        with open(path.join(environ["YZSHELL_TEMPLATES_DIR"], t), "r") as f:
            s = chevron.render(f, data)
        with open(path.join(environ["YZSHELL_TEMPLATE_CACHE_DIR"], config["colourscheme"], templates[t]), "w") as f:
            f.write(s)