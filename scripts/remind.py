#!/usr/bin/env python

# i know this script fucking sucks lmaoo

from time import sleep
from os import environ
import json
from datetime import datetime
import subprocess


if __name__ == "__main__":
    while True:
        reminders = None
        try:
            with open(environ["YZSHELL_REMINDERS_FILE"], "r") as f:
                try:
                    reminders = json.load(f)
                except:
                    print(
                        "Warning: invalid file at " 
                        + environ["YZSHELL_REMINDERS_FILE"]
                    )
        except:
            pass
        if reminders != None:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            for r in reminders:
                if now == r["date"]:
                    subprocess.Popen(
                        f"notify-send 'Reminders' '{r["content"].replace("'", "\\'")}' --wait",
                        shell=True
                    )

        sleep(60)