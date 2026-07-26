from bs4 import BeautifulSoup
from os import environ, path
import subprocess

class Labwc:
    def __init__(self, config):
        self._config = config
    
    def configure(self):
        # rc.xml
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
        binds.append(f'''
            <keybind key="W-p">
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

        for b in binds:
            soup.keyboard.append(BeautifulSoup(b, "xml"))
        with open(dest, "w") as f:
            f.write(soup.decode())
            
        #self.reload()

    def reload(self):
        subprocess.run(
            f"labwc -r", 
            shell=True, stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )
