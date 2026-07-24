import subprocess
from sys import exit
import subprocess


class EwwDaemon:
    def __init__(self, modules = {}):
        self.modules = modules

    def launch(self):
        try:
            subprocess.run(
                "eww daemon", 
                shell=True, stdout=subprocess.DEVNULL, 
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
            shell=True, stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )
    
    def update_var(self, var, val):
        subprocess.run(
            f"eww update {var}='{val}'", 
            shell=True, stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )

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
                shell=True, stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT
            )
        except:
            print("Error: could not open widget '{self.name}'")
            exit(1)
        for p in self.pre_open:
            p()
        subprocess.run(
            f"eww update {self.name}_visible=true", 
            shell=True, stdout=subprocess.DEVNULL, 
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
            print("Error: could not open widget '{self.name}'")
            exit(1)
