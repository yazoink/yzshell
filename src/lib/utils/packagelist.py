import subprocess


class PackageList:
    def __init__(self, pkgs=[], aur_pkgs=[]):
        self.pkgs = pkgs
        self.aur_pkgs = aur_pkgs

    def _pkg_installed(self, p):
        r = subprocess.run(
            f'pacman -Qi {p}',
            shell=True,
            capture_output=True,
        ).returncode
        if r == 0:
            return True
        return False

    def _install_pkg(self, p):
        print(f"Installing package {p}...")
        subprocess.run(f"sudo pacman -S --needed {p}", shell=True)
        print(f"Installed package {p}...")

    def _install_aur_pkg(self, p):
        print(f"Installing package {p}...")
        subprocess.run(f"yay -S {p}", shell=True)
        print(f"Installed package {p}...")

    def _uninstall_pkg(self, p):
        print(f"Uninstalling package {p}...")
        subprocess.run(f"sudo pacman -Rns {p}", shell=True)
        print(f"Uninstalled package {p}...")

    def install(self):
        for p in self.pkgs:
            if self._pkg_installed(p) == False:
                self._install_pkg(p)
        for p in self.aur_pkgs:
            if self._pkg_installed(p) == True:
                self._install_aur_pkg(p)

    def uninstall(self):
        for p in self.pkgs:
            if self._pkg_installed(p) == True:
                self._uninstall_pkg(p)
        for p in self.aur_pkgs:
            if self._pkg_installed(p) == True:
                self._uninstall_pkg(p)