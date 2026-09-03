#!/usr/bin/env python

import subprocess
import json

# get workspaces
wspaces = sorted(
    json.loads(subprocess.run(
        "hyprctl workspaces -j",
        shell=True,
        text=True,
        capture_output=True
    ).stdout.strip()),
    key=lambda d: d["name"]
)

# remove special workspace
i = 0
for w in wspaces:
    if "special:special" in w["name"]:
        wspaces.pop(i)
        break
    i += 1

wspaces_num = len(wspaces)
spacing = 8
max_height = 725
wspace_btn_height = 125
active_wspace = subprocess.run(
    "hyprctl activeworkspace -j | jq -r '.name'",
    shell=True,
    text=True,
    capture_output=True
).stdout.strip()


height = (wspace_btn_height * wspaces_num) + (spacing * (wspaces_num + 1))
if height > max_height:
    height = max_height

subprocess.run(
    f"eww update workspaces_height={str(height)}; eww update active_workspace={active_wspace}",
    shell=True
)
print(json.dumps(wspaces))