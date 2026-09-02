#!/usr/bin/env python

from requests import get
from subprocess import run

r = ""
try:
    r = get("https://api.open-meteo.com/v1/forecast?latitude=-37.814&longitude=144.9633&hourly=temperature_2m&current=temperature_2m,precipitation,cloud_cover,apparent_temperature,wind_speed_10m,is_day&timezone=auto&forecast_days=3")
except:
    print("Error: could not update weather")
    exit(0)

r = r.json()

temp = r["current"]["temperature_2m"]
unit = r["current_units"]["temperature_2m"]

a_temp = r["current"]["apparent_temperature"]
a_unit = r["current_units"]["apparent_temperature"]

rain = r["current"]["precipitation"]
cloud = r["current"]["cloud_cover"]
is_day = r["current"]["is_day"]

icon = ""
colour = ""

if rain > 0.1:
    colour = "blue"
    if is_day == 1:
        icon = ""
    else:
        icon = ""
else:
    if cloud > 50:
        if is_day == 1:
            colour = "yellow"
            icon = ""
        else:
            colour = "blue"
            icon = ""
    else:
        if is_day == 1:
            colour = "yellow"
            icon = ""
        else:
            colour = "blue"
            icon = ""

timezone = r["timezone"]
timezone_abv = r["timezone_abbreviation"]

run(
    f'''
    eww update weather_temp='{temp}{unit}'
    eww update weather_apparent_temp='Feels like {a_temp}{a_unit}'
    eww update weather_icon='{icon}'
    eww update weather_colour='{colour}'
    eww update weather_tz='{timezone} ({timezone_abv})'
    ''',
    shell=True,
)