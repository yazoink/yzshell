from lib.modules.waybar import Waybar
from sys import argv, exit

def main():
    w = Waybar()
    argc = len(argv)

    if argc < 2:  
        w.reload()
        exit(0)

    match argv[1]:
        case "set_show_battery":
            if argc < 3:
                print("Error: not enough args")
                exit(1)
            w.set_show_battery(argv[2])
        case "set_show_backlight":
            if argc < 3:
                print("Error: not enough args")
                exit(1)
            print(argv[2])
            w.set_show_backlight(argv[2])
        case "kill":
            w.kill()
        case "reload":
            w.reload()
        case "configure":
            w.configure()
                

main()