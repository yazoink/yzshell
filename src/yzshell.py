from sys import exit, argv
from threading import Thread
from os import environ, path, listdir, makedirs
from shutil import copytree, rmtree
from time import sleep
import argparse
import subprocess

class Shell:
    def __init__(self):
        self.config = None
        self.osd = None
        self.bar = None
        self.widgets = None
        self.wallpaper = None
        self.windowmanager = None
        self.notifs = None
        self.colourscheme = None
        self.default_apps = None

    def _set_osd(self):
        from lib.modules.swayosd import SwayOSD
        if self.osd == None:
            self.osd = SwayOSD()

    def _set_bar(self):
        from lib.modules.waybar import Waybar
        if self.bar == None:
            self.bar = Waybar(self.config)

    def _set_widgets(self):
        from lib.modules.eww import Eww
        if self.widgets == None:
            self.widgets = Eww(self.config)

    def _set_wallpaper(self):
        from lib.modules.wallpaper import Wallpaper
        if self.wallpaper == None:
            self.wallpaper = Wallpaper(self.config)

    def _set_windowmanager(self):
        from lib.modules.labwc import Labwc
        if self.windowmanager == None:
            self.windowmanager = Labwc(self.config)

    def _set_notifs(self):
        from lib.modules.mako import Mako
        if self.notifs == None:
            self.notifs = Mako()

    def _set_config(self):
        from lib.utils.config import Config
        if self.config == None:
            self.config = Config()

    def _set_default_apps(self):
        from lib.utils.defaultapps import DefaultApps
        if self.default_apps == None:
            self.default_apps = DefaultApps(self.config)

    def _set_colourscheme(self, scheme):
        from lib.utils.colourscheme import Colourscheme
        if self.colourscheme == None:
            self.colourscheme = Colourscheme(scheme)

    def get_default_app_categories(self):
        self._set_config()
        self._set_default_apps()
        for category in self.default_apps.apps:
            print(category)

    def get_available_default_apps(self, category):
        self._set_config()
        self._set_default_apps()
        if category not in self.default_apps.apps:
            print("Error: category '{category}' does not exist")
        for a in self.default_apps.apps[category]:
            print(a)

    def pick_colour(self, sleep_time=0):
        sleep(sleep_time)
        r = subprocess.run(
            "hyprpicker",
            shell=True,
            text=True,
            capture_output=True
        )
        if r.returncode == 0:
            colour = r.stdout.strip()
            subprocess.Popen(
                f"wl-copy '{colour}'",
                shell=True,
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT
            )
            subprocess.Popen(
                f"notify-send '{colour}' 'Copied to clipboard'",
                shell=True,
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT
            )

    def get_config_opt(self, opt):
        self._set_config()
        self.config.get(opt)

    def set_config_opt(self, opt, val):
        self._set_config()
        self.config.change(opt, val)

    def install_all_default_apps(self):
        self._set_config()
        self._set_default_apps()
        self.default_apps.install_all()

    def change_default_app(self, category, app):
        self._set_config()
        self._set_default_apps()
        self._set_windowmanager()
        self.default_apps.change(category, app)
        self.windowmanager.configure()
        self.windowmanager.reload()

    def set_wallpaper_image(self, image):
        if path.isfile(image) == False:
            print(f"Error: file '{image}' not found")
            exit(1)
        self._set_config()
        self._set_widgets()
        self._set_wallpaper()
        i = path.abspath(image)
        s = path.split(i)
        self.widgets.update_var("current_wallpaper", s[0])
        self.config.change("wallpaper_image", s[1])
        if s[0] != self.config.current["wallpaper_dir"]:
            self.config.change("wallpaper_dir", s[0])
            self.widgets.update_var("wallpaper_dir", s[0])
            self.widgets.update_available_wallpapers(s[0])
            self.widgets.update_wallpaper_thumbs()
        self.wallpaper.reload()

    def set_wallpaper_mode(self, mode):
        self._set_config()
        self._set_widgets()
        self._set_wallpaper()
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
        self.widgets.update_var("wallpaper_mode", mode)
        self.config.change("wallpaper_mode", mode)
        self.wallpaper.reload()

    def get_search_results(self, query=""):
        self._set_widgets()
        self.widgets.get_search_results(query)

    def update_weather(self):
        self._set_widgets()
        self.widgets.update_weather()

    def update_search_cache(self):
        self._set_widgets()
        self.widgets.update_search_cache()

    def toggle_dnd(self):
        self._set_widgets()
        mode = subprocess.run(
            "makoctl mode",
            shell=True, 
            text=True,
            capture_output=True
        ).stdout
        if "do-not-disturb" in mode:
            subprocess.run(
                "makoctl mode -r do-not-disturb",
                shell=True, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT
            )
            subprocess.Popen(
                "notify-send 'Notifications' 'Do not disturb disabled'",
                shell=True, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT
            )
        else:
            subprocess.run(
                "makoctl mode -a do-not-disturb",
                shell=True, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT
            )
        self.widgets.get_dnd_icon()

    def update_wallpaper_thumbs(self, dir=None):
        self._set_config()
        self._set_widgets()
        if dir == None:
            self.widgets.update_wallpaper_thumbs()
        else:
            self.widgets.update_wallpaper_thumbs(dir)

    def update_available_wallpapers(self, dir=None):
        self._set_config()
        self._set_widgets()
        if dir == None:
            self.widgets.update_available_wallpapers()
        else:
            self.widgets.update_available_wallpapers(dir)

    def lock_screen(self):
        subprocess.Popen(
            f"swaylock -f -c 000000", 
            shell=True, stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )

    def screenshot(self, output, mode, sleep_time):
        self._set_config()
        sleep(sleep_time)
        if output == None:
            date = subprocess.run(
                "date +%Y%m%d_%H:%M:%S",
                shell=True,
                capture_output=True
            ).stdout
            dir = self.config.current["screenshot_dir"]
            output = f"{dir}/{date}.png"
        else:
            s = path.split(output)
            dir = s[0]
        if path.exists(dir) == False:
            makedirs(dir)
        if mode == "full":
            r = subprocess.run(
                f"grim {output}", 
                shell=True, 
                capture_output=True
            )
        elif mode == "select":
            r = subprocess.run(
                f"grim -g \"$(slurp)\" {output}",
                shell=True, 
                capture_output=True
            )
        else:
            arg_not_recognised(mode)
        if r.returncode == 0:
            subprocess.run(
                f"notify-send -i {output} 'Screenshot saved' '{output}'",
                shell=True, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT
            )

    def launch(self):
        self._set_config()
        self._set_wallpaper()
        self._set_osd()
        self._set_bar()
        self._set_windowmanager()
        self._set_notifs()
        self._set_wallpaper()
        self._set_widgets()
        Thread(target=self.widgets.reload).start()
        Thread(target=self.wallpaper.reload).start()
        Thread(target=self.osd.reload).start()
        Thread(target=self.bar.reload).start()
        Thread(target=self.windowmanager.reload).start()
        Thread(target=self.notifs.reload).start()

    def open(self, widget):
        self._set_config()
        self._set_widgets()
        self.widgets.modules[widget].open()

    def close(self, widget):
        self._set_widgets()
        self.widgets.modules[widget].close()

    def toggle(self, widget):
        self._set_config()
        self._set_widgets()
        self.widgets.modules[widget].toggle()

    def reconfigure(self):
        self._set_config()
        self._set_default_apps()
        self._set_bar()
        self._set_windowmanager()

        def write_config(cfg):
            src = f"{environ["STATIC_CONFIG_DIR"]}/.config/{cfg}"
            dest = f"{environ["CONFIG_DIR"]}/{cfg}"
            s = path.split(dest)
            if path.isfile(src):
                write_file(src, dest)
            else:
                try:
                    rmtree(dest)
                except:
                    pass
                copytree(src, dest)
            print(f"Copied '{src}' to {dest}")

        def configure_vencord():
            cfg = ""
            try:
                makedirs(f"{environ["CONFIG_DIR"]}/Vencord/settings")
            except:
                pass
            with open(f"{environ["TEMPLATES_DIR"]}/vencord_settings.json", "r") as f:
                cfg = f.read()
            with open(f"{environ["CONFIG_DIR"]}/Vencord/settings/settings.json", "w") as f:
                f.write(cfg)
            print("Configured Vencord")

        if path.exists(environ["CONFIG_DIR"]) == False:
            makedirs(environ["CONFIG_DIR"])
            
        write_file(f"{environ["STATIC_CONFIG_DIR"]}/.zshrc", f"{environ["HOME"]}/.zshrc")
        write_file(f"{environ["STATIC_CONFIG_DIR"]}/.zprofile", f"{environ["HOME"]}/.zprofile")

        configs = listdir(f"{environ["STATIC_CONFIG_DIR"]}/.config")
        threads = []
        for cfg in configs:
            threads.append(Thread(target=write_config, args=(cfg,)))
            write_config(cfg)
        threads.append(Thread(target=self.default_apps.configure))
        threads.append(Thread(target=self.bar.configure))
        threads.append(Thread(target=self.windowmanager.configure))
        
        for t in threads:
            t.start()

        for t in threads:
            t.join()

        configure_vencord()

        self.reconfigure_colourscheme()

    def reconfigure_colourscheme(self, scheme=None):
        from lib.utils.colourscheme import MustacheTemplate

        self._set_config()
        if scheme == None:
            scheme = self.config.current["colourscheme"]
        self._set_colourscheme(scheme)

        templates = [
            MustacheTemplate("eww.scss.mustache", f"{environ["CONFIG_DIR"]}/eww/scss/_colours.scss"),
            MustacheTemplate("foot.ini.mustache", f"{environ["CONFIG_DIR"]}/foot/foot.ini"),
            MustacheTemplate("gtk.css.mustache", f"{environ["CONFIG_DIR"]}/gtk-3.0/gtk.css"),
            MustacheTemplate("gtk.css.mustache", f"{environ["CONFIG_DIR"]}/gtk-4.0/gtk.css"),
            MustacheTemplate("kvantum.kvconfig.mustache", f"{environ["CONFIG_DIR"]}/Kvantum/KvRecolour/KvRecolour.kvconfig"),
            MustacheTemplate("kvantum.svg.mustache", f"{environ["CONFIG_DIR"]}/Kvantum/KvRecolour/KvRecolour.svg"),
            MustacheTemplate("labwc_themerc.mustache", f"{environ["CONFIG_DIR"]}/labwc/themerc-override"),
            MustacheTemplate("mako.mustache", f"{environ["CONFIG_DIR"]}/mako/config"),
            MustacheTemplate("waybar.css.mustache", f"{environ["CONFIG_DIR"]}/waybar/colours.css"),
            MustacheTemplate("wofi.css.mustache", f"{environ["CONFIG_DIR"]}/wofi/style.css"),
            MustacheTemplate("yazi.toml.mustache", f"{environ["CONFIG_DIR"]}/yazi/theme.toml"),
            MustacheTemplate("swayosd.css.mustache", f"{environ["CONFIG_DIR"]}/swayosd/style.css"),
            MustacheTemplate("zen_userchrome.css.mustache", f"{self.config.current["zen_profile_dir"]}/chrome/userChrome.css"),
            MustacheTemplate("zen_usercontent.css.mustache", f"{self.config.current["zen_profile_dir"]}/chrome/userContent.css"),
            MustacheTemplate("zathurarc.mustache", f"{environ["CONFIG_DIR"]}/zathura/zathurarc"),
            MustacheTemplate("discord.css.mustache", f"{environ["CONFIG_DIR"]}/Vencord/themes/yzshell.theme.css"),
        ]
        threads = []
        for t in templates:
            threads.append(Thread(target=t.apply, args=(self.colourscheme,)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.config.change("colourscheme", scheme)

def arg_not_recognised(arg):
    print(f"Error: argument '{arg}' not recognised")
    exit(1)

def not_enough_args(cmd):
    print(f"Error: not enough args to '{cmd}'")
    exit(1)

def too_many_args(cmd):
    print(f"Error: too many args to '{cmd}'")
    exit(1)

def write_file(src, dest):
    content = ""
    with open(src, "r") as f:
        content = f.read()
    with open(dest, "w") as f:
        f.write(content)

if __name__ == "__main__":
    argc = len(argv)
    shell = Shell()
    if argc == 1: # launch yzshell
        shell.launch()
    else:
        cmd = argv[1]
        match cmd:
            case "open":
                if argc < 3:
                    not_enough_args(cmd)
                elif argc > 3:
                    too_many_args(cmd)
                else:
                    shell.open(argv[2])
            case "close":
                if argc < 3:
                    not_enough_args(cmd)
                elif argc > 3:
                    too_many_args(cmd)
                else:
                    shell.close(argv[2])
            case "toggle":
                if argc < 3:
                    not_enough_args(cmd)
                elif argc > 3:
                    too_many_args(cmd)
                else:
                    shell.toggle(argv[2])
            case "reconfigure":
                reload = False
                if argc > 2:
                    if argc > 3:
                        too_many_args(cmd)
                    match argv[2]:
                        case "-r" | "--reload":
                            reload = True
                        case _:
                            arg_not_recognised(argv[2])
                shell.reconfigure()
                if reload == True:
                    shell.launch()
            case "colourscheme":
                if argc < 3:
                    not_enough_args(cmd)
                elif argc > 3:
                    too_many_args(cmd)
                else:
                    shell.reconfigure_colourscheme(argv[2])
                    shell.launch()
            case "config":
                if argc < 3:
                    not_enough_args(cmd)
                else:
                    action = argv[2]
                    match action:
                        case "get":
                            if argc < 4:
                                not_enough_args(action)
                            if argc > 4:
                                too_many_args(action)
                            shell.get_config_opt(argv[3])
                        case "set":
                            if argc < 5:
                                not_enough_args(action)
                            if argc > 5:
                                too_many_args(action)
                            shell.set_config_opt(argv[3], argv[4])
                        case _:
                            arg_not_recognised(action)
            case "default_apps":
                if argc < 3:
                    not_enough_args(cmd)
                action = argv[2]
                match action:
                    case "install_all":
                        shell.install_all_default_apps()
                    case "get":
                        if argc < 4:
                            not_enough_args(cmd)
                        match argv[3]:
                            case "categories":
                                if argc > 4:
                                    too_many_args(argv[3])
                                shell.get_default_app_categories()
                            case "apps":
                                if argc < 5:
                                    not_enough_args(argv[3])
                                if argc > 5:
                                    too_many_args(argv[3])
                                shell.get_available_default_apps(argv[4])
                            case _:
                                arg_not_recognised(argv[3])
                    case "set":
                        if argc < 5:
                            not_enough_args(cmd)
                        shell.change_default_app(argv[3], argv[4])
                    case _:
                        arg_not_recognised(action)
            case "toggle_dnd":
                shell.toggle_dnd()
            case "get_search_results":
                query = ""
                if argc > 2:
                    if argc > 3:
                        too_many_args(cmd)
                    query = argv[2]
                shell.get_search_results(query)
            case "update_search_cache":
                if argc > 2:
                    too_many_args(cmd)
                shell.update_search_cache()
            case "update_weather":
                if argc > 2:
                    too_many_args(cmd)
                shell.update_weather()
            case "set_wallpaper":
                if argc < 3:
                    not_enough_args(cmd)
                elif argc > 3:
                    too_many_args(cmd)
                else:
                    shell.set_wallpaper_image(argv[2])
            case "set_wallpaper_mode":
                if argc < 3:
                    not_enough_args(cmd)
                elif argc > 3:
                    too_many_args(cmd)
                else:
                    shell.set_wallpaper_mode(argv[2])
            case "update_wallpaper_thumbs":
                if argc < 3:
                    shell.update_wallpaper_thumbs()
                elif argc > 3:
                    too_many_args(cmd)
                else:
                    shell.update_wallpaper_thumbs(argv[2])
            case "update_available_wallpapers":
                if argc < 3:
                    shell.update_available_wallpapers()
                elif argc > 3:
                    too_many_args(cmd)
                else:
                    shell.update_available_wallpapers(argv[2])
            case "lock":
                shell.lock_screen()
            case "screenshot":
                parser = argparse.ArgumentParser(add_help=False)
                parser.add_argument("-m", "--mode", default="full")
                parser.add_argument("-o", "--output", default=None)
                parser.add_argument("-s", "--sleep-time", default=0, type=float)
                args = parser.parse_args(argv[2:])
                shell.screenshot(
                    output=args.output,
                    mode=args.mode,
                    sleep_time=args.sleep_time
                )
            case "pick_colour":
                parser = argparse.ArgumentParser(add_help=False)
                parser.add_argument("-s", "--sleep-time", default=0, type=float)
                args = parser.parse_args(argv[2:])
                shell.pick_colour(sleep_time=args.sleep_time)
            case _:
                arg_not_recognised(cmd)