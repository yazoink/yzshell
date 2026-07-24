from lib.utils.config import Config
from sys import argv, exit

def main():
    argc = len(argv)
    if argc < 2:
        print("Error: not enough args")
        exit(1)
    c = Config()
    match argv[1]:
        case "get_option":
            if argc < 3:
                print("Error: not enough args")
                exit(1)
            if argv[2] not in c.current:
                print(f"Error: config option '{argv[2]}' does not exist")
                exit(1)
            print(c.current[argv[2]])
        case "get_default_option":
            if argc < 3:
                print("Error: not enough args")
                exit(1)
            if argv[2] not in c.defaults:
                print(f"Error: config option '{argv[2]}' does not exist")
                exit(1)
            print(c.defaults[argv[2]])
        case "set_option":
            if argc < 4:
                print("Error: not enough args")
                exit(1)
            c.change(argv[2], argv[3])
            print(f"Set config option '{argv[2]}' to '{argv[3]}'")


main()