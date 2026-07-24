import subprocess
from sys import exit
from os import environ, path, listdir, makedirs
from shutil import rmtree
from lib.utils.config import Config
from lib.modules.eww import EwwDaemon
from PIL import Image

class Wallpaper:
    def __init__(self, config=Config(), eww=EwwDaemon()):
        self._config = config
        self._eww = eww

    def update_thumbs(self, dir = ""):
        if dir == "":
            dir = self._config.current["wallpaper_dir"]
        files = listdir(dir)

        #if path.exists(environ["WALLPAPER_CACHE_DIR"]) == True:
        #    rmtree(environ["WALLPAPER_CACHE_DIR"])
        if path.exists(environ["WALLPAPER_CACHE_DIR"]) == False:
            makedirs(environ["WALLPAPER_CACHE_DIR"])

        for f in files:
            l = f.lower()
            if l.endswith(('.jpg', '.png', '.jpeg')):
                with Image.open(path.join(self._config.current["wallpaper_dir"], f)) as i:
                    MAX_SIZE = (150, 150)
                    i.thumbnail(MAX_SIZE)
                    i.save(path.join(environ["WALLPAPER_CACHE_DIR"], f))

    def set_image(self, image):
        i = path.abspath(image)
        if path.isfile(i) == False:
            print(f"Error: file '{i}' not found")
            exit(1)
        s = path.split(i)
        self._config.change("wallpaper_image", s[1])
        self._config.change("wallpaper_dir", s[0])
        self.reload()

        self._eww.update_var("current_wallpaper", f"{s[0]}/{s[1]}")

    def set_mode(self, mode):
        modes = [
            "stretch",
            "fit",
            "fill",
            "center",
            "tile"
        ]
        if mode not in modes:
            print(f"Error: mode '{mode}' invalid")
            exit(1)
        self._config.change("wallpaper_mode", mode)
        self._eww.update_var("wallpaper_mode", mode)

        self.reload()

    def reload(self):
        self.kill()
        self.launch()

    def launch(self):
        i = self._config.current["wallpaper_image"]
        d = self._config.current["wallpaper_dir"]
        m = self._config.current["wallpaper_mode"]
        try:
            r = subprocess.Popen(
                f"swaybg -i '{d}/{i}' -m '{m}'", 
                shell=True, stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT
            )
        except:
            print("Error: could not set wallpaper")
            exit(1)

    def kill(self):
        r = subprocess.run(
            f"killall swaybg", 
            shell=True, stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )