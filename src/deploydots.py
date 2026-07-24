from os import environ, path, listdir, makedirs
from shutil import copytree, rmtree, copyfile
from sys import exit, argv
from lib.modules.waybar import Waybar
from lib.modules.labwc import Labwc
from lib.utils.config import Config
from lib.utils.defaultapps import DefaultApps
import subprocess

def write_file(src, dest):
    cfg = ""
    with open(src, "r") as f:
        cfg = f.read()
    with open(dest, "w") as f:
        f.write(cfg)


# deploy/reconfigure dotfiles
def main():
    argc = len(argv)
    cfg = Config()
    default_apps = DefaultApps(cfg)

    if argc > 1:
        match argv[1]:
            case "ensure_default_apps":
                default_apps.install_packages()
            case "clean_default_apps":
                default_apps.clean_packages()

    if path.exists(environ["CONFIG_DIR"]) == False:
        makedirs(environ["CONFIG_DIR"])
        
    write_file(f"{environ["STATIC_CONFIG_DIR"]}/.zshrc", f"{environ["HOME"]}/.zshrc")
    write_file(f"{environ["STATIC_CONFIG_DIR"]}/.zprofile", f"{environ["HOME"]}/.zprofile")

    configs = listdir(f"{environ["STATIC_CONFIG_DIR"]}/.config")
    for c in configs:
        src = f"{environ["STATIC_CONFIG_DIR"]}/.config/{c}"
        dest = f"{environ["CONFIG_DIR"]}/{c}"
        if path.isfile(src):
            write_file(src, dest)
        else:
            if path.exists(dest) == True:
                rmtree(dest)
            copytree(src, dest)
        print(f"Copied '{src}' to {dest}")

    default_apps.write_mimeapps_list()
    Waybar(cfg).configure()
    Labwc(cfg).configure()

main()