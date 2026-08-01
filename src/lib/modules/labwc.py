from os import environ, path
import subprocess


class Labwc:
    def __init__(self, config):
        self._config = config
    
    def configure(self):
        from bs4 import BeautifulSoup
        menu_xml = subprocess.run(
            f"labwc-menu-generator -I -t '{self._config.current["terminal"]} -e'", 
            shell=True, 
            text=True,
            capture_output=True
        ).stdout.strip()
        with open(f"{environ["CONFIG_DIR"]}/labwc/menu.xml", "w") as f:
            f.write(menu_xml)
        src = path.join(environ["STATIC_CONFIG_DIR"], ".config/labwc/rc.xml")
        dest = path.join(environ["CONFIG_DIR"], "labwc/rc.xml")
        data = ""
        with open(src, "r") as f:
            data = f.read()
        soup = BeautifulSoup(data, "xml")
        binds = []
        binds.append(f'''
            <keybind key="W-Return">
                <action name="Execute" command="{self._config.current["terminal"]}" />
            </keybind>''' 
        )
        binds.append(f'''
            <keybind key="W-w">
                <action name="Execute" command="{self._config.current["web_browser"]}" />
            </keybind>'''
        )
        binds.append(f'''
            <keybind key="W-e">
                <action name="Execute" command="{self._config.current["file_manager"]}" />
            </keybind>'''
        )
        binds.append(f'''
            <keybind key="W-r">
                <action name="Execute" command="{self._config.current["run_launcher"]}" />
            </keybind>'''
        )

        soup.desktops["number"] = self._config.current["labwc_desktops"]
        for i in range(1, self._config.current["labwc_desktops"] + 1):
            binds.append(f'''<keybind key="W-{i}">
                <action name="GoToDesktop" to="{i}" />
            </keybind>''')
            binds.append(f'''<keybind key="W-S-{i}">
                <action name="SendToDesktop" to="{i}" />
            </keybind>''')

        soup.libinput.device.scrollFactor.string = str(self._config.current["touchpad_scroll_factor"])

        for b in binds:
            soup.keyboard.append(BeautifulSoup(b, "xml"))
        with open(dest, "w") as f:
            f.write(soup.decode())
            
        #self.reload()
        src = f"{environ["TEMPLATES_DIR"]}/zprofile.mustache"
        dest = f"{environ["HOME"]}/.zprofile"
        with open(src, "r") as f:
            cfg = f.read()
        cfg = cfg.replace("{{window_manager}}", "labwc")
        with open(dest, "w") as f:
            f.write(cfg)

    def reload(self):
        subprocess.run(
            f"labwc -r", 
            shell=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )
