#!/usr/bin/env python

import heapq
import json
import subprocess
from collections import deque
from os import path
from sys import exit

NOTES_FILE = path.expanduser("~/.notes.md")


def get_yzshell_data():
    return json.loads(
        subprocess.run(
            ["yzconf", "dump_mustache_data"], capture_output=True, text=True
        ).stdout.strip()
    )


# function stolen from failedex
def parse_line(line, n):
    # (char, position)
    special = {
        "*": "i",
        "_": "i",
        "**": "b",
        "~~": "s",
        "__": "u",
    }
    stack = deque()

    change = []

    for i in range(len(line)):

        cand = line[i : i + n]

        if cand in special.keys():
            if len(stack) != 0 and stack[-1][0] == cand:
                char, j = stack.pop()
                heapq.heappush(change, (-j, f"<{special[char]}>"))
                heapq.heappush(change, (-i, f"</{special[char]}>"))
            else:
                stack.append((cand, i))

    while len(change) != 0:
        i, char = heapq.heappop(change)
        line = line[:-i] + char + line[-i + n :]

    return line


def parse_file():
    pango = ""
    yzshell_data = get_yzshell_data()
    with open(NOTES_FILE, "r") as f:
        for line in f.readlines():
            words = line.split()
            if len(words) == 0:
                pango += "\n"
                continue
            if words[0] == "#":
                pango += (
                    f"<span weight='bold' color='{yzshell_data["accent-hex"]}' size='19pt'><span size='15pt' font_family='Font Awesome 7 Free'> </span>"
                    + " ".join(words[1:])
                    + "</span>\n"
                )
                continue
            if words[0] == "##":
                pango += (
                    f"<span weight='bold' color='{yzshell_data["accent-hex"]}' size='17pt'><span size='13pt' font_family='Font Awesome 7 Free'> </span>"
                    + " ".join(words[1:])
                    + "</span>\n"
                )
                continue
            if words[0] == "###":
                pango += (
                    f"<span weight='bold' color='{yzshell_data["accent-hex"]}' size='15pt'><span size='11pt' font_family='Font Awesome 7 Free'> </span>"
                    + " ".join(words[1:])
                    + "</span>\n"
                )
                continue
            if words[0] == "-":
                if words[1].lower() == "[x]":
                    words = words[1:]
                    words[0] = (
                        f"<span weight='bold' color='{yzshell_data["accent-hex"]}' size='13pt' font_family='Font Awesome 7 Free'> </span>"
                    )
                elif words[1] == "[" and words[2] == "]":
                    words = words[2:]
                    words[0] = (
                        f"<span size='13pt' font_family='Font Awesome 7 Free'> </span>"
                    )
                else:
                    words[0] = (
                        f"<span weight='bold' color='{yzshell_data["accent-hex"]}' font_family='Font Awesome 7 Free'>- </span>"
                    )
            line = " ".join(words)
            line = parse_line(line, 2)
            line = parse_line(line, 1)
            pango += line + "\n"

        return pango


if __name__ == "__main__":
    if path.isfile(NOTES_FILE) == False:
        print('<span fgalpha="40%"><i>Nothing here...</i></span>')
        exit(0)

    pango = parse_file()
    print(pango)
