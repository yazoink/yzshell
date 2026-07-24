from os import environ, path
import subprocess

class Swaylock:
    def __init__(self):
        pass

    def launch(self):
        subprocess.Popen(
            f"swaylock -f -c 000000", 
            shell=True, stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )
