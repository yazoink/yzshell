#!/usr/bin/env python

from os import path, remove, unlink
from shutil import rmtree

def delete_if_exists(p):
    if path.isdir(p) == True:
        rmtree(p)
    elif path.isfile(p) == True:
        remove(p)
    elif path.islink(p) == True:
        unlink(p)


def get_full_path(p):
    if "~" in p:
        return path.expanduser(p)
    else:
        return path.abspath(p)