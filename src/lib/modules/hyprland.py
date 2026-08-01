from os import environ, path
import subprocess


class Hyprland:
    def __init__(self, config):
        self._config = config
    
    def configure(self):
        sf = str(self._config.current["touchpad_scroll_factor"])
        src = f"{environ["STATIC_CONFIG_DIR"]}/.config/hypr/input.lua"
        dest = f"{environ["CONFIG_DIR"]}/hypr/input.lua"
        cfg = ""
        with open(src, "r") as f:
            cfg = f.read()
        cfg.replace("scroll_factor = 0.15", "scroll_factor = {sf}")
        with open(dest, "w") as f:
            f.write(cfg)

    def reload(self):
        subprocess.run(
            f"hyprctl reload; hyprpm reload", 
            shell=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )
