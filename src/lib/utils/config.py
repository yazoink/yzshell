from os import path, environ, makedirs
import json
from sys import exit

class Config:
    def __init__(self):
        self.defaults = {
            "colourscheme": "camellia",
            "bar_show_battery": False,
            "bar_show_backlight": True,
            "profile_image": f"{environ["DATA_DIR"]}/assets/images/profile_image.jpg",
            "screenshot_dir": f"{environ["HOME"]}/pic/screenshots",
            "wallpaper_dir": f"{environ["DATA_DIR"]}/assets/images/wallpapers",
            "wallpaper_image": "dolphins-tile.png",
            "wallpaper_mode": "tile",
            "zen_profile_dir": f"{environ["HOME"]}/.config/zen/gd1z8qc7.Default (release)",
            "file_manager": "pcmanfm",
            "web_browser": "zen",
            "document_reader": "zathura",
            "terminal": "foot",
            "media_player": "mpv",
            "image_viewer": "imv",
            "run_launcher": "wofi --show run",
            "labwc_desktops": 9,
            "touchpad_scroll_factor": 0.15,
            "oh_my_zsh_theme": "robbyrussell",
            "enable_h264ify": False,
        }
        self.current = self.defaults

        if path.isfile(environ["YZSHELL_CONFIG_FILE"]):
            user_config = {}
            with open(environ["YZSHELL_CONFIG_FILE"], "r") as f:
                j = f.read()
                try:
                    user_config = json.loads(j)
                except:
                    print(f"Error: could not load config at '{environ["YZSHELL_CONFIG_FILE"]}', please check for errors")
                    exit(1)
            for opt in user_config:
                self.current[opt] = user_config[opt]

    def get(self, opt):
        if opt not in self.current:
            print(f"Error: option '{opt}' does not exist")
            exit(1)
        print(self.current[opt])

    def change(self, opt, val):
        if opt not in self.defaults:
            print(f"Error: config option '{opt}' does not exist")
            exit(1)
        if type(self.defaults[opt]) != type(val):
            print(f"Error: invalid value for '{opt}'")
            exit(1)
        self.current[opt] = val
        if path.exists(environ["YZSHELL_CONFIG_DIR"]) == False:
            makedirs(environ["YZSHELL_CONFIG_DIR"])
        with open(environ["YZSHELL_CONFIG_FILE"], "w") as f:
            f.write(json.dumps(self.current))
