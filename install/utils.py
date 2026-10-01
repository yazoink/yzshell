#!/usr/bin/env python

import subprocess
from os import path

def install_pkgs(pkgs):
    subprocess.run(
        f"sudo pacman -S --needed --noconfirm {" ".join(pkgs)}",
        shell=True
    )


def confirm(question):
    a = subprocess.run(
        f'gum confirm --padding="1 1" "{question}"', 
        shell=True
    )
    if a.returncode == 0:
        return True
    return False


def get_input(question):
    return subprocess.run(
        f"gum input --placeholder '{question}'", 
        shell=True, 
        text=True, 
        stdout=subprocess.PIPE
    ).stdout.strip()


def choose(x, opts):
    cmd = f"gum choose --padding='1 1' --header 'Select {x}...'"
    for o in opts:
        cmd += f" '{o}'"
    return subprocess.run(
        cmd, shell=True, text=True, stdout=subprocess.PIPE
    ).stdout.strip()


def update_config(opt, val):
    subprocess.run(["yzconf", "set", opt, val])

def install_pkgs(pkgs, aur=False):
    cmd = [
        "pacman", 
        "-S",
        "--needed",
        "--noconfirm"
    ]
    if aur == True:
        cmd[0] = "yay"
        cmd.extend(["--norebuild", "--noredownload"])
    else:
        cmd.insert(0, "sudo")
    l = len(cmd)
    for p in pkgs:
        if pkg_installed(p, aur) == False:
            cmd.append(p)
    if len(cmd) > l:
        subprocess.run(cmd)

def pkg_installed(pkg, aur=False):
    mgr_cmd = "pacman"
    if aur == True:
        mgr_cmd = "yay"
    r = subprocess.run(
        [mgr_cmd, "-Qi", pkg],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    if r.returncode == 0:
        return True
    else:
        return False

def set_env_vars(env_vars):
    env_file = "/etc/environment"
    tmp_file = "/tmp/yzshell_env"
    lines = []

    if path.isfile(env_file) == False:
        subprocess.run(["sudo", "touch", env_file])

    for v in env_vars:
        subprocess.run(
            f"""
            if grep "{v}" "{env_file}"; then
                sudo gawk -i inplace "!/{v}/" "{env_file}"
            fi
            echo "{v}={env_vars[v]}" \
                | sudo tee -a "{env_file}"
            """,
            shell=True,
            capture_output=True
        )

def remove_pkgs(pkgs, aur=False):
    cmd = [
        "pacman", 
        "-Rns",
        "--noconfirm"
    ]
    if aur == True:
        cmd[0] = "yay"
    else:
        cmd.insert(0, "sudo")
    l = len(cmd)
    for p in pkgs:
        if pkg_installed(p, aur):
            cmd.append(p)
    if len(cmd) > l:
        subprocess.run(cmd)