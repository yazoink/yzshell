import subprocess
from sys import exit
from os import environ, path

def make_thumb(f):
        with Image.open(path.join(self._config.current["wallpaper_dir"], f)) as i:
            MAX_SIZE = (150, 150)
            i.thumbnail(MAX_SIZE)
            i.save(path.join(environ["WALLPAPER_CACHE_DIR"], f))

class Wallpaper:
    def __init__(self, config):
        self._config = config

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
                shell=True, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT
            )
        except:
            print("Error: could not set wallpaper")
            exit(1)

    def kill(self):
        r = subprocess.run(
            f"killall swaybg", 
            shell=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )