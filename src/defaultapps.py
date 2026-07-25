from sys import exit, argv
from lib.utils.defaultapps import DefaultApps
from lib.utils.config import Config

def main():
    argc = len(argv)
    cfg = Config()
    default_apps = DefaultApps(cfg)

    if argc > 1:
        match argv[1]:
            case "install_all":
                default_apps.install_all()
            case "change":
                if argc > 3:
                    default_apps.change(argv[2], argv[3])
    else:
        print("Error: not enough args")
        exit(1)

main()