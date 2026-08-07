import subprocess
from sys import exit

class SwayOSD:
    def __init__(self):
        pass

    def kill(self):
        subprocess.run(
            f"killall swayosd-server", 
            shell=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )

    def launch(self):
        subprocess.Popen(
            f"swayosd-server", 
            shell=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )

    def reload(self):
        self.kill()
        self.launch()