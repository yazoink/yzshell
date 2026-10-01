#!/usr/bin/env python

import json
from sys import argv, exit
from utils import install_pkgs

file = None
deps = None

if len(argv) < 2:
    print("Error: please specify file")
    exit(1)

with open(argv[1], "r") as f:
    deps = json.load(f)

install_pkgs(deps["pacman"])
install_pkgs(deps["yay"], aur=True)