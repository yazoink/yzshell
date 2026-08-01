from os import environ, path
import subprocess


class Hyprland:
    def __init__(self, config):
        self._config = config
    
    def configure(self):
        src = f"{environ["TEMPLATES_DIR"]}/hyprland_vars.lua.mustache"
        dest = f"{environ["CONFIG_DIR"]}/hypr/vars.lua"
        cfg = ""
        with open(src, "r") as f:
            cfg = f.read()
        cfg = cfg.replace(
            "{{touchpad_scroll_factor}}", 
            str(self._config.current["touchpad_scroll_factor"])
        )
        cfg = cfg.replace(
            "{{web_browser}}", 
            str(self._config.current["web_browser"])
        )
        cfg = cfg.replace(
            "{{terminal}}", 
            str(self._config.current["terminal"])
        )
        cfg = cfg.replace(
            "{{file_manager}}", 
            str(self._config.current["file_manager"])
        )
        cfg = cfg.replace(
            "{{run_launcher}}", 
            str(self._config.current["run_launcher"])
        )
        with open(dest, "w") as f:
            f.write(cfg)

        src = f"{environ["TEMPLATES_DIR"]}/zprofile.mustache"
        dest = f"{environ["HOME"]}/.zprofile"
        with open(src, "r") as f:
            cfg = f.read()
        cfg = cfg.replace("{{window_manager}}", "start-hyprland")
        with open(dest, "w") as f:
            f.write(cfg)

    def reload(self):
        subprocess.run(
            f"hyprctl reload; hyprpm reload", 
            shell=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )
