#!/usr/bin/env python

import json
import time
from argparse import ArgumentParser
from sys import argv, exit

import requests


def get_unit(arg):
    match arg:
        case "celsius":
            return "C"
        case "farenheit":
            return "F"
        case _:
            print(f"Error: invalid unit: {args.unit}")
            exit(1)


def get_data():
    try:
        data = json.loads(requests.get("https://wttr.in/?format=j1", timeout=15).text)
    except:
        print("Error: could not update weather")
        exit(1)
    return data


def get_icon(data, day):
    # day
    code_icon = {
        113: "",  # clear
        116: "",  # few clouds
        119: "",  # clouds
        122: "",  # clouds
        143: "",  # fog
        176: "",  # rain
        179: "",  # snow
        182: "",  # snow
        185: "",  # snow
        200: "",  # storm
        227: "",  # snow
        230: "",  # storm
        248: "",  # fog
        260: "",  # fog
        263: "",  # rain light
        266: "",  # rain light
        281: "",  # rain light
        284: "",  # rain light
        293: "",  # rain light
        296: "",  # rain light
        299: "",  # rain
        302: "",  # rain
        305: "",  # rain
        308: "",  # rain
        311: "",  # rain
        353: "",  # rain light
        356: "",  # rain
    }

    # night
    code_icon_n = {
        113: "",  # clear
        116: "",  # few clouds
        119: "",  # clouds
        122: "",  # clouds
        143: "",  # fog
        176: "",  # rain
        179: "",  # snow
        182: "",  # snow
        185: "",  # snow
        200: "",  # storm
        227: "",  # snow
        230: "",  # storm
        248: "",  # fog
        260: "",  # fog
        263: "",  # rain light
        266: "",  # rain light
        281: "",  # rain light
        284: "",  # rain light
        293: "",  # rain light
        296: "",  # rain light
        299: "",  # rain
        302: "",  # rain
        305: "",  # rain
        308: "",  # rain
        311: "",  # rain
        353: "",  # rain light
        356: "",  # rain
    }

    code = int(data["current_condition"][0]["weatherCode"])
    if day:
        if code in code_icon:
            return code_icon[code]
    else:
        if code in code_icon_n:
            return code_icon_n[code]
    print(f"Error: invalid weather code: {str(code)}")
    exit(1)


def get_colour(data, day):
    colour = None
    rain = float(data["current_condition"][0]["precipMM"])
    cloud = int(data["current_condition"][0]["cloudcover"])
    if rain > 0.1:  # raining
        colour = "cyan"
    else:  # not raining
        if cloud > 50:  # cloudy
            colour = "purple"
        else:  # not cloudy
            if day:
                colour = "yellow"
            else:
                colour = "blue"
    return colour


def main():
    curr_time = time.localtime()
    day = 6 < curr_time.tm_hour < 20
    temp = None
    aparr_temp = None
    area = None

    # args
    parser = ArgumentParser()
    parser.add_argument("-u", "--unit", default="celsius")
    args = parser.parse_args(argv[1:])

    unit = get_unit(args.unit)
    data = get_data()

    icon = get_icon(data, day)
    temp = data["current_condition"][0][f"temp_{unit}"]
    aparr_temp = data["current_condition"][0][f"FeelsLike{unit}"]
    area = data["nearest_area"][0]["areaName"][0]["value"]
    country = data["nearest_area"][0]["country"][0]["value"]
    colour = get_colour(data, day)

    r = {
        "icon": icon,
        "temp": f"{temp}°{unit}",
        "appar_temp": f"Feels like {aparr_temp}°{unit}",
        "location": f"{area}, {country}",
        "day": day,
        "colour": colour,
    }

    print(json.dumps(r))


main()
