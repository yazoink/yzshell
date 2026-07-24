from lib.modules.wallpaper import Wallpaper
from sys import argv, exit


def main():
    w = Wallpaper()
    argc = len(argv)

    if argc < 2:  
        w.reload()
        exit(0)

    match argv[1]:
        case "update_thumbs":
            w.update_thumbs()
        case "set_image":
            if argc < 3:
                print("Error: not enough args")
                exit(1)
            w.set_image(argv[2])
        case "set_mode":
            if argc < 3:
                print("Error: not enough args")
                exit(1)
            print(argv[2])
            w.set_mode(argv[2])
            eww.update_var("wallpaper_fill", argv[2])
        case "kill":
            w.kill()
        case "reload":
            w.reload()
                

main()