import subprocess
from sys import exit

class Mako:
    def __init__(self):
        pass

    def kill(self):
        subprocess.run(
            f"killall mako", 
            shell=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )

    def launch(self):
        subprocess.Popen(
            f"mako", 
            shell=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )

    def reload(self):
        subprocess.Popen(
            f"makoctl reload", 
            shell=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )