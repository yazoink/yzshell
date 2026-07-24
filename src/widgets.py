from lib.modules.eww import EwwWindow, EwwDaemon
from lib.utils.config import Config
from sys import argv, exit
import subprocess
from os import environ, path, listdir, makedirs
import json

class Widgets(EwwDaemon):
    def __init__(self, config=Config()):
        self._config = config
        super().__init__(
            modules={
                "calendar": EwwWindow("calendar"),
                "power": EwwWindow("power"),
                "screenshot": EwwWindow(
                    name="screenshot",
                    post_open=[self.update_screenshot_output]
                ),
                "settings": EwwWindow(
                    name="settings",
                    post_open=[
                        self.get_colourschemes,
                        self.get_wallpapers
                    ],
                ),
                "control_center": EwwWindow(
                    name="control_center",
                    pre_launch=[
                        self.update_search_cache,
                    ],
                    pre_open=[
                        self.get_dnd_icon, 
                        self.get_profile_image, 
                    ],
                    post_open=[
                        self.get_search_results, 
                        self.update_weather
                    ],
                )
            },
        )

    def update_screenshot_output(self):
        d = self._config.current["screenshot_dir"]
        date = subprocess.run("date +%d-%m-%Y_%H:%M:%S", shell=True, capture_output=True, text=True).stdout.strip()
        if path.exists(d) == False:
            makedirs(d)
        out_path = path.join(d, f"{date}_screenshot.png")
        self.update_var("output", out_path)

    def get_colourschemes(self):
        print("CONFIG: " + str(self._config.current))
        schemes_list = listdir(environ["COLOURS_DIR"])

        colourschemes = []
        for sch in schemes_list:
            j = ""
            with open(f"{environ["COLOURS_DIR"]}/{sch}", "r") as f:
                j = f.read()
            j = json.loads(j)
            j["id"] = sch.replace(".json", "")
            colourschemes.append(j)

        self.update_var("colourschemes", json.dumps(colourschemes))


    def get_wallpapers(self):
        self.update_var("wallpaper_dir", self._config.current["wallpaper_dir"])
        wallpapers = subprocess.run(
            f"\"$HOME\"/.config/eww/settings/scripts/get_available_wallpapers.py '{self._config.current["wallpaper_dir"]}'", 
            shell=True, 
            capture_output=True,
            text=True
        ).stdout.strip()
        self.update_var("wallpapers", wallpapers)
        self.update_var("current_wallpaper", path.join(self._config.current["wallpaper_dir"], self._config.current["wallpaper_image"]))
        self.update_var("wallpaper_mode", self._config.current["wallpaper_mode"])


    def get_dnd_icon(self):
        subprocess.run(
            f"{environ["CONFIG_DIR"]}/eww/control_center/scripts/get_dnd_icon.sh",
            shell=True, stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )

    def update_weather(self):
        subprocess.Popen(
            f"{environ["CONFIG_DIR"]}/eww/control_center/scripts/weather.sh",
            shell=True, stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )

    def get_profile_image(self):
        self.update_var("profile_image_path", self._config.current["profile_image"])

    def update_search_cache(self):
        subprocess.Popen(
            f"{environ["CONFIG_DIR"]}/eww/control_center/scripts/search.py update_cache",
            shell=True, stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )

    def get_search_results(self):
        subprocess.Popen(
            f"{environ["CONFIG_DIR"]}/eww/control_center/scripts/search.py get_results",
            shell=True, stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )


def main():
    config = Config()
    eww = Widgets(config)
    eww.update_screenshot_output()
    argc = len(argv)
    if argc < 2:
        eww.kill()
        eww.launch()
        exit(0)
    if argv[1] == "kill":
        eww.kill()
        exit(0)
    if argc < 3:
        print("Error: not enough args")
        exit(1)
    w = None
    for m in eww.modules:
        if m == argv[1]:
            w = eww.modules[m]
    if w != None:
        match argv[2]:
            case "open":
                w.open()
            case "close":
                w.close()
            case "toggle":
                w.toggle()
            


main()