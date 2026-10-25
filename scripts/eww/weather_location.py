#!/usr/bin/env python

import requests
from sys import argv, exit
import json
import subprocess

if __name__ == "__main__":
    if len(argv) < 2:
        print("Error: no location specicied")
        exit(1)

    subprocess.run(
        "eww update setting_weather=true",
        shell=True
    )

    location = argv[1]
    if location == "":
        location = "default"

    print(location)

    try:
        l = location
        if location == "default":
            l = ""
        _ = json.loads(requests.get(
            f"https://wttr.in/{l}?format=j1", 
            timeout=15
        ).text)
    except:
        print("Error: invalid location")
        subprocess.run(
            """
            eww update weather_location="$(yzconf get weather_location)"
            eww update setting_weather=false
            notify-send "Location invalid!" "Could not update settings"
            """,
            shell=True
        )
        exit(1)
    subprocess.run(
        f"""
        eww update weather_location="{location}"
        yzconf set weather_location "{location}"
        eww poll weather_data
        eww update setting_weather=false
        #notify-send "Weather" "Location set to {location}"
        """,
        shell=True
    )