#!/usr/bin/env python

from sys import argv
import subprocess

current = argv[1]
next = argv[2]
eww_var = argv[3]

t = None

if current > next:
    t = "slideright"
else:
    t = "slideleft"

subprocess.run(
    f'''eww update stack_transition="{t}"
    eww update {eww_var}={next}''', 
    shell=True
    )