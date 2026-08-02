from lib.utils.windowmanager import WindowManager

class Hyprland(WindowManager):
    def __init__(self, config):
        from lib.utils.packagelist import PackageList
        super().__init__(
            name = "hyprland",
            config = config,
            launch_cmd="start-hyprland",
            reload_cmd = "hyprctl reload",
            deps=PackageList([
                "hyprland",
                "hyprpolkitagent",
                "xdg-desktop-portal-hyprland",
                "pkgconf",
                "cpio",
                "cmake",
                "git",
                "meson",
                "gcc"
            ])
        )

    def configure(self):
        from os import environ
        src = f"{environ["TEMPLATES_DIR"]}/hyprland_vars.lua.mustache"
        dest = f"{environ["CONFIG_DIR"]}/hypr/hyprland/vars.lua"
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
        print("Hyprland configured")