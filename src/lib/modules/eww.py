import subprocess
from sys import exit
import subprocess
from os import environ, path, listdir, makedirs
from math import floor
from PIL import Image
from threading import Thread
import json
from gi.repository import Gio
import re
import requests

class EwwDaemon:
    def __init__(self, modules={}):
        self.modules = modules

    def launch(self):
        try:
            subprocess.run(
                "eww daemon", 
                shell=True, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT
            )
        except:
            print("Error: could not open widgets")
            exit(1)
        for m in self.modules:
            self.modules[m].launch()

    def kill(self):
        subprocess.run(
            "killall eww", 
            shell=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )
    
    def reload(self):
        self.kill()
        self.launch()
    
    def update_var(self, var, val):
        r = subprocess.run(
            f"eww update {var}='{val}'", 
            shell=True, 
            capture_output=True
        )
        if r.returncode != 0:
            print(r.stderr)
            print("Error: could not update variable")
            exit(1)

class EwwWindow:
    def __init__(self, name, pre_launch = [], pre_open = [], post_open = []):
        self.name = name
        self.pre_launch = pre_launch
        self.pre_open = pre_open
        self.post_open = post_open

    def launch(self):
        for p in self.pre_launch:
            p()

    def toggle(self):
        r = subprocess.run(
                f"eww active-windows | grep {self.name}",
                shell=True,
                capture_output=True
        )
        if r.returncode == 0:
            self.close()
        else:
            self.open()

    def open(self):
        try:
            subprocess.run(
                f"eww open '{self.name}'", 
                shell=True, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT
            )
        except:
            print(f"Error: could not open widget '{self.name}'")
            exit(1)
        for p in self.pre_open:
            p()
        subprocess.run(
            f"eww update {self.name}_visible=true", 
            shell=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )
        for p in self.post_open:
            p()

    def close(self):
        try:
            subprocess.Popen(
                f"eww update {self.name}_visible=false; sleep 0.5; eww close '{self.name}' &", 
                shell=True, stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT
            )
        except:
            print(f"Error: could not open widget '{self.name}'")
            exit(1)


class Eww(EwwDaemon):
    def __init__(self, config):
        self._config = config
        self._search_cache_file = "/tmp/yzshell_search_cache.json"
        self._all_apps = []
        super().__init__(
            modules={
                "calendar": EwwWindow("calendar"),
                "power": EwwWindow("power"),
                "screenshot": EwwWindow(
                    name="screenshot",
                    post_open=[Thread(target=self.update_screenshot_output).start]
                ),
                "settings": EwwWindow(
                    name="settings",
                    pre_launch=[Thread(target=self.update_wallpaper_thumbs).start],
                    pre_open=[Thread(target=self.wallpaper_settings_init).start],
                    post_open=[
                        Thread(target=self.get_colourschemes).start
                    ],
                ),
                "control_center": EwwWindow(
                    name="control_center",
                    pre_launch=[
                        self.update_search_cache,
                    ],
                    pre_open=[
                        Thread(target=self.get_dnd_icon).start, 
                        Thread(target=self.get_profile_image).start, 
                        Thread(target=self.get_search_results).start
                    ],
                    post_open=[
                        Thread(target=self.update_weather).start
                    ],
                )
            },
        )

    def _make_thumb(self, f):
        with Image.open(path.join(self._config.current["wallpaper_dir"], f)) as i:
            MAX_SIZE = (150, 150)
            i.thumbnail(MAX_SIZE)
            i.save(path.join(environ["WALLPAPER_CACHE_DIR"], f))

    def update_wallpaper_thumbs(self, dir=""):
        print("Updating wallpaper thumbnails...")
        if dir == "":
            dir = self._config.current["wallpaper_dir"]
        files = listdir(dir)

        if path.exists(environ["WALLPAPER_CACHE_DIR"]) == False:
            makedirs(environ["WALLPAPER_CACHE_DIR"])
        for f in files:
            l = f.lower()
            if l.endswith(('.jpg', '.png', '.jpeg')):
                Thread(target=self._make_thumb, args=(f,)).start()

    def update_screenshot_output(self):
        d = self._config.current["screenshot_dir"]
        date = subprocess.run(
            "date +%d-%m-%Y_%H:%M:%S", 
            shell=True, 
            capture_output=True, 
            text=True
        ).stdout.strip()
        if path.exists(d) == False:
            makedirs(d)
        out_path = path.join(d, f"{date}_screenshot.png")
        self.update_var("output", out_path)

    def get_colourschemes(self):
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

    def update_available_wallpapers(self, dir=None):
        if dir == None:
            dir = self._config.current["wallpaper_dir"]
        self.update_var("wallpaper_dir", dir)
        columns = 3
        files = listdir(dir)
        # print(files)

        available_wallpapers = []
        col = 0
        row = 0

        i = 0
        image_files = []
        for f in files:
            if f.endswith(('.jpg', '.png', '.jpeg')):
                image_files.append(f)

        if len(image_files) < 3:
            rows = 1
        else:
            rows = floor(len(files) / 3)

        i = 0
        for row in range(0, rows):
            cols = 3
            available_wallpapers.append([])
            for _ in range(0, cols):
                if i < len(image_files):
                    available_wallpapers[row].append(image_files[i])
                    i += 1

        #print(json.dumps(available_wallpapers))
        self.update_var("wallpapers", json.dumps(available_wallpapers))

    def wallpaper_settings_init(self):
        self.update_available_wallpapers()
        self.update_var("current_wallpaper", path.join(self._config.current["wallpaper_dir"], self._config.current["wallpaper_image"]))
        self.update_var("wallpaper_mode", self._config.current["wallpaper_mode"])

    def get_dnd_icon(self):
        mode = subprocess.run(
            "makoctl mode",
            shell=True, 
            text=True,
            capture_output=True
        ).stdout
        print(mode)
        if "do-not-disturb" in mode:
            self.update_var("dnd_icon", "")
        else:
            self.update_var("dnd_icon", "")

    def update_weather(self):
        r = ""
        try:
            r = requests.get("https://api.open-meteo.com/v1/forecast?latitude=-37.814&longitude=144.9633&hourly=temperature_2m&current=temperature_2m,precipitation,cloud_cover,apparent_temperature,wind_speed_10m,is_day&timezone=auto&forecast_days=3")
        except:
            print("Error: could not update weather")
            exit(0)

        r = r.json()

        temp = r["current"]["temperature_2m"]
        unit = r["current_units"]["temperature_2m"]
        self.update_var("weather_temp", f"{temp}{unit}")

        temp = r["current"]["apparent_temperature"]
        unit = r["current_units"]["apparent_temperature"]
        self.update_var("weather_apparent_temp", f"Feels like {temp}{unit}")

        rain = r["current"]["precipitation"]
        cloud = r["current"]["cloud_cover"]
        is_day = r["current"]["is_day"]

        icon = ""
        colour = ""

        if rain > 0.1:
            colour = "base0D"
            if is_day == 1:
                icon = ""
            else:
                icon = ""
        else:
            if cloud > 50:
                if is_day == 1:
                    colour = "base0A"
                    icon = ""
                else:
                    colour = "base0D"
                    icon = ""
            else:
                if is_day == 1:
                    colour = "base0A"
                    icon = ""
                else:
                    colour = "base0D"
                    icon = ""
        self.update_var("weather_icon", icon)
        self.update_var("weather_colour", colour)

        timezone = r["timezone"]
        timezone_abv = r["timezone_abbreviation"]
        self.update_var("weather_tz", f"{timezone} ({timezone_abv})")

    def get_profile_image(self):
        self.update_var("profile_image_path", self._config.current["profile_image"])

    def update_search_cache(self):
        def add_app(app, i):
            if app.should_show() == False:
                return
            cmd = ""
            if app.get_boolean("Terminal"):
                cmd = f"{environ["TERM"]} -e "
            cmd += app.get_commandline()
            cmd = re.sub("%[a-zA-Z]", "", cmd)
            cmd = re.sub(" -- $", "", cmd)
            icon = "question"
            icon_obj = app.get_icon()
            if icon_obj != None:
                icon = Gio.Icon.to_string(icon_obj)
            desc = app.get_description()
            if desc == None:
                desc = "No description"
            self._all_apps.append(
                {
                    "name": app.get_display_name(),
                    "desc": desc,
                    "cmd": cmd, # launch command
                    "icon": icon,
                    "bin": app.get_executable(), # base binary file
                    "index": i,
                }
            )
        app_info = Gio.AppInfo.get_all()
        i = 0
        threads = []
        for app in app_info:
            threads.append(Thread(target=add_app, args=(app, i,)))
            i += 1
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        j = json.dumps(self._all_apps)
        with open(self._search_cache_file, "w") as f:
            f.write(j)

    def get_search_results(self, query=""):
        r = ""
        selected = -1
        # load cached app array
        if self._all_apps == []:
            if path.isfile(self._search_cache_file) == False:
                self.update_search_cache()
            else:
                with open(self._search_cache_file, "r") as f:
                    j = f.read()
                    self._all_apps = json.loads(j)

        # if empty search, return all
        if query.replace(" ", "") == "":
            r = json.dumps(self._all_apps)
        else:
            selected = 0
            # get results array    
            results = []
            for a in self._all_apps:
                n = a["name"].lower()
                d = a["desc"].lower()
                if query in n or query in d:
                    if n.startswith(query):
                        results.insert(0, a)
                    else:
                        results.append(a)
            
            # re-index
            for i in range(0, len(results)):
                results[i]["index"] = i
            #print(results)
            r = json.dumps(results)
        #print(r)
        self.update_var("search_results", r)
        self.update_var("search_selected", str(selected))