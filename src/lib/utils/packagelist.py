import subprocess

class PackageList():
    def __init__(self, pkgs):
        self.pkgs = pkgs

    def _pkg_installed(self, p):
        r = subprocess.run(
            f"xbps-query -l | grep -q \"ii {p}-[0-9]\"",
            shell=True,
            capture_output=True,
        ).returncode
        if r == 0:
            return True
        return False

    def _install_pkg(self, p):
        print(f"Installing package {p}...")
        subprocess.run(
            f"sudo xbps-install -y {p}",
            shell=True
        )
        print(f"Installed package {p}...")

    def _uninstall_pkg(self, p):
        print(f"Uninstalling package {p}...")
        subprocess.run(
            f"sudo xbps-remove -o -y {p}",
            shell=True
        )
        print(f"Uninstalled package {p}...")

    def install(self):
        for p in self.pkgs:
            if self._pkg_installed(p) == False:
                self._install_pkg(p)

    def uninstall(self):
        for p in self.pkgs:
            if self._pkg_installed(p) == True:
                self._uninstall_pkg(p)