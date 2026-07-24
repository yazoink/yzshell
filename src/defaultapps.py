from sys import exit, argv
from lib.utils.defaultapps import DefaultApps
from lib.utils.config import Config

def main():
    argc = len(argv)
    cfg = Config()
    default_apps = DefaultApps(cfg)

    if argc > 1:
        match argv[1]:
            case "ensure_packages":
                default_apps.install_packages()
            case "clean_packages":
                default_apps.clean_packages()
            case "change":
                if argc > 3:
                    default_apps.change_default(argv[2], argv[3])
    else:
        print("Error: not enough args")
        exit(1)

main()