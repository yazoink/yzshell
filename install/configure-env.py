#!/usr/bin/env python

from os import path, makedirs, environ

script_dir = path.join(environ["TARGET_DIR"], "scripts")
lib_dir = path.join(environ["TARGET_DIR"], "lib")
conf_dir = path.expanduser("~/.config/yzshell")
cache_dir = path.expanduser("~/.cache/yzshell")
env_vars = {
    "YZSHELL_DATA_DIR": environ["TARGET_DIR"],
    "YZSHELL_ENV_FILE": environ["ENV_FILE"],
    "YZSHELL_LIB_DIR": lib_dir,
    "YZSHELL_PYTHON_LIB_DIR": path.join(lib_dir, "python"),
    "YZSHELL_BASH_LIB_DIR": path.join(lib_dir, "bash"),
    "YZSHELL_STOW_DIR": path.expanduser("~/.dotfiles"),
    "YZSHELL_CONF_DIR": conf_dir,
    "YZSHELL_CONF_FILE": path.join(conf_dir, "config.json"),
    "YZSHELL_DEFAULT_CONF_FILE": path.join(environ["TARGET_DIR"], "misc/default-config.json"),
    "YZSHELL_EWW_DIR": path.expanduser("~/.config/eww"),
    "YZSHELL_SCRIPT_DIR": script_dir,
    "YZSHELL_EWW_SCRIPT_DIR": path.join(script_dir, "eww"),
    "YZSHELL_COLOURS_DIR": path.join(environ["TARGET_DIR"], "colourschemes"),
    "YZSHELL_TEMPLATES_DIR": path.join(environ["TARGET_DIR"], "templates"),
    "YZSHELL_CACHE_DIR": cache_dir,
    "YZSHELL_TEMPLATE_CACHE_DIR": path.join(cache_dir, "built_templates"),
    "YZSHELL_WALLPAPER_CACHE_DIR": path.join(cache_dir, "wallpapers"),
    "YZSHELL_WALLPAPER_LOCKFILE": path.join(cache_dir, "wallpapers.lock"),
}

dir = path.dirname(environ["ENV_FILE"])
if path.exists(dir) == False:
    makedirs(dir)

content = ""
for v in env_vars:
    content += f"export {v}={env_vars[v]}\n"
with open(environ["ENV_FILE"], "w") as f:
    f.write(content)