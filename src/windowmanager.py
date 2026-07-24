from sys import argv, exit
from lib.modules.labwc import Labwc

def main():
    wm = Labwc()
    argc = len(argv)

    if argc < 2:  
        wm.reload()
        exit(0)

    match argv[1]:
        case "reload":
            wm.reload()
        case "configure":
            wm.configure()
                

main()