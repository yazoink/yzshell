#!/usr/bin/env python

import json
import subprocess
from sys import argv, exit

file = None
deps = None

if len(argv) < 2:
    print("Error: please specify file")
    exit(1)
print(argv[1])

with open(argv[1], "r") as f:
    deps = json.load(f)

subprocess.run(
    f"sudo pacman -S --needed --noconfirm {" ".join(deps["pacman"])}",
    shell=True
)
subprocess.run(
    f"""
    yay -S \
        --needed \
        --noconfirm \
        --norebuild \
        --noredownload \
        {" ".join(deps["yay"])}
    """,
    shell=True
)