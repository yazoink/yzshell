#!/usr/bin/env python

from os import environ, path, makedirs
import json
from sys import exit, stderr

def get_default_config():
    with open(environ["YZSHELL_DEFAULT_CONF_FILE"], "r") as f:
        return json.load(f)
    # NOTE:
    # Commenting here instead of the file since json doesn't support comments 
    # lol
    #
    # Other good mono fonts aside from default
    # - M+1Code Nerd Font Mono (ttf-mplus-nerd)
    # - Monofur Nerd Font (ttf-monofur-nerd)


def get_config():
    current = get_default_config()
    if path.isfile(environ["YZSHELL_CONF_FILE"]):
        buf = None
        with open(environ["YZSHELL_CONF_FILE"], "r") as f:
            buf = f.read()
        try:
            user_config = json.loads(buf)
            for c in user_config:
                current[c] = user_config[c]
        except json.JSONDecodeError as e:
            print("Warning: could not parse yzshell config, please check for errors. Falling back to default...", e)
    return current


def set_config_option(cfg, opt, val):
    if opt not in cfg:
        print(f"Error: invalid configuration option '{opt}'", file=stderr)
        exit(1)
    cfg[opt] = val
    return cfg


def write_config(cfg):
    if path.exists(environ["YZSHELL_CONF_DIR"]) == False:
        makedirs(environ["YZSHELL_CONF_DIR"])
    with open(environ["YZSHELL_CONF_FILE"], "w") as f:
        f.write(json.dumps(cfg, indent=4))


def get_mustache_data(cfg=None, sch=None):
    if cfg == None:
        cfg = get_config()
    if sch == None:
        sch = get_colourscheme(cfg["colourscheme"])
    data = cfg | sch
    data["prefer_dark_theme"] = "false"
    data["icon_theme"] = "Papirus"
    data["cursor_theme"] = "BreezeX"
    if sch["polarity"] == "dark":
        data["prefer_dark_theme"] = "true"
        data["icon_theme"] += "-Dark"
        data["cursor_theme"] += "-Dark"
    elif sch["polarity"] == "light":
        data["icon_theme"] += "-Light"
        data["cursor_theme"] += "-Light"
    return data


def get_colourscheme(name):
    def hex_to_rgb(hex_colour):
        return tuple(int(hex_colour[i : i + 2], 16) for i in (0, 2, 4))

    def rgb_to_hex(rgb):
        return "{:02X}{:02X}{:02X}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        
    def overlay_colour(base, overlay, amount):
        base = hex_to_rgb(base)
        overlay = hex_to_rgb(overlay)
        r = base[0] + (overlay[0] - base[0]) * amount
        g = base[1] + (overlay[1] - base[1]) * amount
        b = base[2] + (overlay[2] - base[2]) * amount
        return rgb_to_hex((r, g, b))

    #schemes = listdir(environ["YZSHELL_COLOURS_DIR"])
    cols = [
        "background",
        "foreground",
        "surface1",
        "surface2",
        "surface3",
        "surface4",
        "red",
        "orange",
        "yellow",
        "green",
        "cyan",
        "blue",
        "purple",
        "brown",
        "accent"
    ]
    scheme_file = path.join(environ["YZSHELL_COLOURS_DIR"], f"{name}.json")
    scheme = None
    buf = None
    window_buttons = ["red", "yellow", "green"]
    accent = "blue"

    if path.isfile(scheme_file) == False:
        print(f"Error: colourscheme '{name}' not found", file=stderr)
        exit(1)

    with open(scheme_file, "r") as f:
        buf = f.read()
    try:
        scheme = json.loads(buf)
    except json.JSONDecodeError as e:
        print(f"Error: could not load colourscheme at '{scheme_file}'", file=stderr)
        exit(1)

    for i in range(1, 5):
        scheme[f"surface{i}"] = overlay_colour(scheme["background"], scheme["foreground"], i / 10)

    if "window_buttons" in scheme:
        window_buttons = scheme["window_buttons"]
    else:
        window_buttons = ["red", "yellow", "green"]
    if "accent" in scheme:
        accent = scheme["accent"]
    scheme["window_button1"] = scheme[window_buttons[0]]
    scheme["window_button2"] = scheme[window_buttons[1]]
    scheme["window_button3"] = scheme[window_buttons[2]]
    scheme["accent"] = scheme[accent]

    for c in cols:
        d = scheme[c]
        rgb = hex_to_rgb(d)
        scheme[f"{c}-rgb-r"] = rgb[0]
        scheme[f"{c}-rgb-g"] = rgb[1]
        scheme[f"{c}-rgb-b"] = rgb[2]
        scheme[f"{c}-hex"] = f"#{d}"
        scheme[f"{c}-bgr-hex"] = f"{d[4]}{d[5]}{d[2]}{d[3]}{d[0]}{d[1]}"
    return scheme