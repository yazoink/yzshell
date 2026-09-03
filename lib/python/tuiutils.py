#!/usr/bin/env python

import subprocess

def announce(s):
    cmd = f'gum style --foreground 212 "{s}"'
    subprocess.run(cmd, shell=True)


def print_err(msg, level="fatal"):
    cmd = f"gum log --structured --level='{level}' '{msg}'"
    subprocess.run(cmd, shell=True)


def confirm(question):
    a = subprocess.run(f'gum confirm "{question}"', shell=True)
    if a.returncode == 0:
        return True
    return False


def choose(x, opts):
    cmd = f"gum choose --header 'Select {x}...'"
    for o in opts:
        cmd += f" '{o}'"
    return subprocess.run(
        cmd, shell=True, text=True, stdout=subprocess.PIPE
    ).stdout.strip()