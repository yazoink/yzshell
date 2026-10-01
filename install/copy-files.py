#!/usr/bin/env python

from os import path, makedirs, environ
from shutil import rmtree, copytree
import subprocess
from sys import argv, exit

exes = [
    "yzconf",
    "yzshell",
    "yzwallpaper",
    "yzwidgets",
    "yzpicker",
    "yzrecorder",
    "yzshot",
    "yzctl",
    "zenconf",
    "yzshell-install-hyprland-plugins",
    "base16-to-yzshell-scheme",
    "base16-to-yzshell-template"
]
# required directories in yzshell repo
dirs = [
    "assets",
    "colourschemes",
    "dotfiles",
    "templates",
    "misc",
    "scripts",
    "lib",
    "install"
]
data_dir = environ["TARGET_DIR"]
source_dir = environ["REPO_DIR"]

if path.exists(data_dir):
    rmtree(data_dir)
for d in dirs:
    c = path.join(source_dir, d)
    v = path.join(data_dir, d)
    copytree(c, v)
    print(f"Copied directory: {c} => {v}")
bin_dir = path.join(data_dir, "bin")
makedirs(bin_dir)
for e in exes:
    tmp_file = path.join("/tmp/", e)
    target = path.join("/usr/bin", e)
    content = f"""#!/usr/bin/env bash
    source '{environ["ENV_FILE"]}'
    {data_dir}/bin/{e} "$@"
    """
    with open(tmp_file, "w") as f:
        f.write(content)
    subprocess.run(
        f"""
        install -Dm755 '{path.join(source_dir, "bin", e)}' '{path.join(bin_dir, e)}'
        chmod u+x '{tmp_file}'
        sudo install -Dm755 '{tmp_file}' '{target}'
        """, shell=True
    )
    print(f"Installed binary: {target}")