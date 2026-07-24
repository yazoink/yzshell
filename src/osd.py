from lib.modules.swayosd import SwayOSD
from sys import argv, exit


def main():
    osd = SwayOSD()
    argc = len(argv)

    if argc < 2:  
        osd.reload()
        exit(0)

    match argv[1]:
        case "kill":
            osd.kill()
        case "reload":
            osd.reload()
                

main()