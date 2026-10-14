#!/usr/bin/env python

from datetime import datetime
from os import environ
import json
from sys import exit, argv
import subprocess


def sort_data(data):
    return sorted(
        data, 
        key=lambda d: d["date"]
    )


def write_data(data):
    with open(environ["YZSHELL_REMINDERS_FILE"], "w") as f:
        json.dump(data, f)


def get_data():
    data = None
    try:
        with open(environ["YZSHELL_REMINDERS_FILE"], "r") as f:
            data = json.load(f)
    except:
        print("[]")
        exit(0)

    sorted_data = sort_data(data)
    if sorted_data != data:
        write_data(sorted_data)
    return sorted_data


def format_data(data):
    r = []
    i = 0
    for d in data:
        date_obj = datetime.strptime(d["date"], "%Y-%m-%d %H:%M")
        r.append({
            "index": i,
            "date": date_obj.strftime("%A %B %d, %Y"),
            "time": date_obj.strftime("%I:%M %p"),
            "content": d["content"],
        })
        i += 1
    return r


def update_eww(var, val, string=False):
    if string == True:
        val=f"\"{val.replace("\"", "\\\"")}\""
    #print(f"eww update {var}={val}")
    subprocess.run(
        f"eww update {var}={val}",
        shell=True
    )


def eww_get(var):
    return subprocess.run(
        ["eww", "get", var],
        text=True,
        capture_output=True
    ).stdout.strip()


def set_years(current_year):
    years = [current_year]
    for i in range(current_year, current_year + 8):
        years.append(i)
    update_eww("reminder_years", json.dumps(years).strip(), string=True)


def set_days(current_month, current_year):
    days_30 = [
        "September",
        "April",
        "June",
        "November"
    ]
    days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    inc = 0
    if current_month == "February":
        if current_year % 4 == 0 and (current_year % 100 != 0 or current_year % 400 == 0):
            days.append(29)
    else:
        if current_month in days_30:
            inc = 2
        else:
            inc = 3
        for i in range(29, 29 + inc):
            days.append(i)
        
    update_eww("reminder_days", json.dumps(days).strip(), string=True)


def init_new_reminder():
    current_year = datetime.now().year
    current_month = datetime.now().strftime("%B")
    current_day = datetime.now().day
    set_years(current_year)
    set_days(current_month, current_year)
    update_eww("reminder_year", str(current_year), string=True)
    update_eww("reminder_day", str(current_day), string=True)
    update_eww("reminder_month", str(current_month), string=True)


if __name__ == "__main__":
    reminders = []
    data = get_data()
    if len(argv) > 1:
        match argv[1]:
            case "update":
                reminders = format_data(data)
                update_eww("reminders", json.dumps(reminders), string=True)
                init_new_reminder()
                update_eww("reminder_content", "", string=True)
                update_eww("reminder_editing", "-1")
            case "add":
                index = int(eww_get("reminder_editing"))
                day = eww_get("reminder_day")
                month = eww_get("reminder_month")
                year = eww_get("reminder_year")
                hour = eww_get("reminder_hour")
                min = eww_get("reminder_min")
                content = eww_get("reminder_content")
                date = datetime.strptime(
                    f"{day} {month} {year} {hour} {min}",
                    "%d %B %Y %H %M"
                ).strftime("%Y-%m-%d %H:%M")
                a = {
                    "date": date,
                    "content": content
                }
                if index == -1:
                    data.append(a)
                else:
                    data[index] = a
                data = sort_data(data)
                write_data(data)
                reminders = format_data(data)
                update_eww("edit_reminder", "false", string=True)
                init_new_reminder()
                update_eww("reminder_content", "", string=True)
                update_eww("reminders", json.dumps(reminders), string=True)
                update_eww("reminder_editing", "-1")
            case "del":
                data.pop(int(argv[2]))
                write_data(data)
                reminders = format_data(data)
                update_eww("reminders", json.dumps(reminders), string=True)
            case "edit":
                i = int(argv[2])
                update_eww("reminder_editing", str(i))
                date = datetime.strptime(data[i]["date"], "%Y-%m-%d %H:%M")
                day = date.strftime("%d")
                month = date.strftime("%B")
                year = date.strftime("%Y")
                hour = date.strftime("%H")
                minute = date.strftime("%M")
                content = data[i]["content"]
                update_eww("reminder_year", str(year), string=True)
                update_eww("reminder_day", str(day), string=True)
                update_eww("reminder_month", str(month), string=True)
                update_eww("reminder_hour", str(hour), string=True)
                update_eww("reminder_min", str(minute), string=True)
                update_eww("reminder_content", content, string=True)
                update_eww("edit_reminder", "true")
            case "dateclicked":
                day = argv[2]
                month = int(argv[3]) + 1
                year = argv[4]
                date = datetime.strptime(f"{day} {month} {year}", "%d %m %Y")
                month = date.strftime("%B")
                update_eww("reminder_year", str(year), string=True)
                update_eww("reminder_day", str(day), string=True)
                update_eww("reminder_month", str(month), string=True)
                update_eww("edit_reminder", "true")
            case "updatedays":
                month = eww_get("reminder_month")
                year = int(eww_get("reminder_year"))
                set_days(month, year)