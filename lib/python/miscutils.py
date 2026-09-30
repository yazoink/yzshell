#!/usr/bin/env python

from os import path, remove
from shutil import rmtree
import subprocess

def delete_if_exists(p):
    subprocess.run(
        f"rm -rf '{p}'",
        shell=True
    )


def get_full_path(p):
    if "~" in p:
        return path.expanduser(p)
    else:
        return path.abspath(p)