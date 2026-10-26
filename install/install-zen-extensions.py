#!/usr/bin/env python

import subprocess
from os import makedirs, path
from sys import argv, exit

import requests

cmd = None
extensions = {
    "uBlock Origin": "uBlock0@raymondhill.net",
    "SponsorBlock": "sponsorBlocker@ajay.app",
    "Stylus": "{7a7a4a92-a2a0-41d1-9fd7-1e92480d612d}",
    "Violentmonkey": "{aecec67f-0d10-4fa7-b7c7-609a2db280cf}",
    "LocalCDN": "{b86e4813-687a-43e6-ab65-0bde4ab75758}",
    "ClearURLs": "{74145f27-f039-47ce-a470-a662b129930a}",
    "Floccus": "floccus@handmadeideas.org",
    "Control Panel for Twitter": "{5cce4ab5-3d47-41b9-af5e-8203eea05245}",
    "Control Panel for YouTube": "control-panel-for-youtube@jbscript.dev",
    "KeePassXC-Browser": "keepassxc-browser@keepassxc.org",
    "I Still Don't Care About Cookies": "idcac-pub@guus.ninja",
    "enhanced-h264ify": "{9a41dee2-b924-4161-a971-7fb35c053a4a}",
}
profile_dir = argv[1]
extensions_dir = path.join(profile_dir, "extensions")

# ensure extensions dir
if path.exists(extensions_dir) == False:
    makedirs(extensions_dir)

# choose extensions
cmd = (
    "gum choose --header 'Select Zen Browser extensions'"
    + " --padding='1 1' --no-limit "
    + '--selected="'
    + ",".join(extensions.keys())
    + '" '
    + " ".join(f"\"{k}\"" for k in extensions.keys())
)
chosen = subprocess.run(
    cmd, 
    shell=True, 
    text=True, 
    stdout=subprocess.PIPE
).stdout.strip().split("\n")
if "" in chosen:
    chosen.remove("")

# add extensions to template
for e in chosen:
    url = f"https://addons.mozilla.org/firefox/downloads/latest/{extensions[e]}/latest.xpi"
    file_path = path.join(extensions_dir, f"{extensions[e]}.xpi")
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Extension downloaded successfully: {url} => {file_path}")
    else:
        print(f"Failed to download file: {url}. Please check your internet connection.")
        exit(1)
