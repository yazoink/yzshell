#!/usr/bin/env python

import subprocess
import json
from sys import argv, exit

# get direction
direction = None
if len(argv) > 1:
    if argv[1] in ("next", "prev"):
        direction = argv[1]
if direction == None:
    print("Error: no direction specified")
    exit(1)

# get currently selected
r = subprocess.run(
    "eww get search_selected", 
    shell=True, 
    text=True, 
    capture_output=True
).stdout.strip()
selected = int(r)

# get target index
if direction == "next":
    r = subprocess.run(
        "eww get search_results", 
        shell=True, 
        text=True, 
        capture_output=True
    ).stdout.strip()
    results = json.loads(r)
    l = len(results)
    if selected < l:
        selected += 1
elif direction == "prev":
    if selected > -1:
        selected -= 1

# update
subprocess.run(
    f"eww update search_selected={str(selected)}",
    shell=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT,
)