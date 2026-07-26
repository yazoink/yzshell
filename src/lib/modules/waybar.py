from os import listdir, environ
import json
import subprocess
from bs4 import BeautifulSoup

class Waybar:
    def __init__(self, config):
        self._config = config

    def launch(self):
        try:
            r = subprocess.Popen(
                f"waybar", 
                shell=True, stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT
            )
        except:
            print("Error: could not open bar")
            exit(1)

    def reload(self):
        self.kill()
        self.launch()

    def kill(self):
        subprocess.run(
            f"killall waybar", 
            shell=True, stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )

    def set_show_battery(self, val):
        if val == "true":
            self._config.set("bar_show_battery", True)
        if val == "false":
            self._config.set("bar_show_battery", False)
        else:
            print(f"Error: value '{val}' not recognised")

    def set_show_backlight(self, val):
        if val == "true":
            self._config.set("bar_show_backlight", True)
        elif val == "false":
            self._config.set("bar_show_backlight", False)
        else:
            print(f"Error: value '{val}' not recognised")

    def configure(self):
        src = f"{environ["STATIC_CONFIG_DIR"]}/.config/waybar/config.jsonc"
        dest = f"{environ["CONFIG_DIR"]}/waybar/config.jsonc"
        cfg = {}
        with open(src, "r") as f:
            cfg = f.read()
            cfg = json.loads(cfg)

        show_battery = self._config.current["bar_show_battery"]
        show_backlight = self._config.current["bar_show_backlight"]
        if show_battery == True:
            cfg["group/quick-access"]["modules"].insert(1, "group/battery-expander")
        if show_backlight == True:
            cfg["group/quick-access"]["modules"].insert(1, "group/backlight-expander")
            
        battery_name = "AC"
        bats = sorted(listdir("/sys/class/power_supply"))
        for b in bats:
            if b.startswith("BAT"):
                battery_name = b
                break
        cfg["battery#icon"]["bat"] = battery_name
        cfg["battery#percentage"]["bat"] = battery_name

        with open(dest, "w") as f:
            f.write(json.dumps(cfg))

        src = f"{environ["STATIC_CONFIG_DIR"]}/.config/waybar/workspaces.xml"
        dest = f"{environ["CONFIG_DIR"]}/waybar/workspaces.xml"
        data = ""
        with open(src, "r") as f:
            data = f.read()
        soup = BeautifulSoup(data, "xml")
        items = []
        for i in range(1, self._config.current["labwc_desktops"] + 1):
            s = f'''<child>
                <object class="GtkMenuItem" id="w-{i}">
                    <property name="label">Workspace {i}</property>
                </object>
            </child>'''
            soup.object.append(BeautifulSoup(s, "xml"))
        with open(dest, "w") as f:
            f.write(soup.decode())
        
        #self.reload()