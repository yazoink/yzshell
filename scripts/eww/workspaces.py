#!/usr/bin/env python

import json
import subprocess


def get_screen():
    monitors = json.loads(
        subprocess.run(
            "hyprctl monitors -j", shell=True, text=True, capture_output=True
        ).stdout.strip()
    )
    for m in monitors:
        if m["focused"] == True:
            return m["id"]


screen = get_screen()
wspaces = []

# get workspaces
all_wspaces = sorted(
    json.loads(
        subprocess.run(
            "hyprctl workspaces -j", shell=True, text=True, capture_output=True
        ).stdout.strip()
    ),
    key=lambda d: d["name"],
)

for w in all_wspaces:
    if w["monitorID"] is not screen:
        continue
    if "special:special" in w["name"]:
        continue
    wspaces.append(w)

wspaces_num = len(wspaces)
spacing = 8
max_height = 725
wspace_btn_height = 125
active_wspace = subprocess.run(
    "hyprctl activeworkspace -j | jq -r '.name'",
    shell=True,
    text=True,
    capture_output=True,
).stdout.strip()


height = (wspace_btn_height * wspaces_num) + (spacing * (wspaces_num + 1))
if height > max_height:
    height = max_height

subprocess.run(
    f"eww update workspaces_height={str(height)}; eww update active_workspace={active_wspace}",
    shell=True,
)
print(json.dumps(wspaces))
