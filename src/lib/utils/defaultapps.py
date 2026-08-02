import subprocess
from sys import exit
from lib.utils.packagelist import PackageList
from os import environ

class DefaultApp():
    def __init__(self, desktop_file, launch_cmd, install, uninstall):
        self.desktop_file = desktop_file
        self._launch_cmd = launch_cmd
        self.install = install
        self.uninstall = uninstall

    def launch(self):
        subprocess.Popen(
            self._launch_cmd, 
            shell=True,
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )

class PCManFM(DefaultApp):
    def __init__(self):
        self.deps = PackageList(
            pkgs=["pcmanfm"]
        )
        super().__init__(
            desktop_file="pcmanfm.desktop",
            launch_cmd="pcmanfm",
            install=self.deps.install,
            uninstall=self.deps.uninstall
        )

class Thunar(DefaultApp):
    def __init__(self):
        self.deps = PackageList(
            pkgs=[
                "thunar",
                "thunar-archive-plugin",
                "thunar-media-tags-plugin",
                "thunar-volman",
                "thunar-shares-plugin",
            ]
        )
        super().__init__(
            desktop_file="thunar.desktop",
            launch_cmd="thunar",
            install=self.deps.install,
            uninstall=self.deps.uninstall
        )

class Zathura(DefaultApp):
    def __init__(self):
        self.deps = PackageList([
            "zathura",
            "zathura-cb",
            "zathura-djvu",
            "zathura-pdf-mupdf",
            "zathura-ps",
        ])
        super().__init__(
            desktop_file="org.pwmt.zathura.desktop",
            launch_cmd="zathura",
            install=self.deps.install,
            uninstall=self.deps.uninstall
        )

class Atril(DefaultApp):
    def __init__(self):
        self.deps = PackageList(["atril"])
        super().__init__(
            desktop_file="atril.desktop",
            launch_cmd="atril",
            install=self.deps.install,
            uninstall=self.deps.uninstall
        )

class Ristretto(DefaultApp):
    def __init__(self):
        self.deps = PackageList(["ristretto"])
        super().__init__(
            desktop_file="org.xfce.ristretto.desktop",
            launch_cmd="ristretto",
            install=self.deps.install,
            uninstall=self.deps.uninstall
        )

class Imv(DefaultApp):
    def __init__(self):
        self.deps = PackageList(["imv"])
        super().__init__(
            desktop_file="imv-dir.desktop",
            launch_cmd="imv-dir",
            install=self.deps.install,
            uninstall=self.deps.uninstall
        )

class Mpv(DefaultApp):
    def __init__(self):
        self.deps = PackageList(["mpv"])
        super().__init__(
            desktop_file="mpv.desktop",
            launch_cmd="mpv",
            install=self.deps.install,
            uninstall=self.deps.uninstall
        )

class Vlc(DefaultApp):
    def __init__(self):
        self.deps = PackageList(["vlc"])
        super().__init__(
            desktop_file="vlc.desktop",
            launch_cmd="vlc",
            install=self.deps.install,
            uninstall=self.deps.uninstall
        )

class Zen(DefaultApp):
    def __init__(self):
        self.deps = PackageList(aur_pkgs=["zen-browser-bin"])
        self.desktop_file_path = f"{environ["HOME"]}/.local/share/applications/zen.desktop"
        super().__init__(
            desktop_file="zen.desktop",
            launch_cmd="zen",
            install=self.deps.install,
            uninstall=self.deps.uninstall
        )

class Firefox(DefaultApp):
    def __init__(self):
        self.deps = PackageList(["firefox"])
        super().__init__(
            desktop_file="firefox.desktop",
            launch_cmd="firefox",
            install=self.deps.install,
            uninstall=self.deps.uninstall
        )

class DefaultApps():
    def __init__(self, config):
        self._config = config
        self.associations = {
            "file_manager": ["inode/directory"],
            "document_reader": [
                "application/pdf",
                "image/vnd.djvu",
                "application/epub+zip"
            ],
            "image_viewer": [
                "image/bmp",
                "image/gif",
                "image/svg+xml",
                "image/tiff",
                "image/png",
                "image/jpeg",
                "image/jp2",
                "image/avif",
                "image/webp",
                "image/heif",
                "image/x-pixmap"
            ],
            "media_player": [
                "video/ogg",
                "video/x-msvideo",
                "video/mpeg",
                "video/quicktime",
                "video/webm",
                "video/x-flv",
                "video/mp4",
                "video/dv",
                "video/mkv",
                "video/3gp",
                "video/3gpp",
                "video/3gpp2",
                "video/mp2t",
                "video/msvideo",
                "video/x-avi",
                "video/x-anim",
                "video/x-flc",
                "video/x-fli",
                "video/x-matroska",
                "video/x-mpeg",
                "video/x-ms-asf",
                "video/x-ms-wmv",
                "video/x-nsv",
                "video/x-ogm+ogg",
                "video/mp4v-es",
                "audio/mp3",
                "audio/mp4",
                "audio/amr",
                "audio/mpeg2",
                "audio/mpeg3",
                "audio/mpegurl",
                "audio/mpg",
                "audio/x-mpg",
                "audio/aac",
                "audio/opus",
                "audio/x-aac",
                "audio/vnd.dolby.heaac.1",
                "audio/vnd.dolby.heaac.2",
                "audio/amr-wb",
                "audio/mpeg",
                "audio/aiff",
                "audio/x-aiff",
                "audio/webm",
                "audio/m4a",
                "audio/mp1",
                "audio/mp2",
                "audio/x-mp1",
                "audio/x-mp2",
                "audio/x-m4a",
                "audio/x-matroska",
                "audio/x-mp3",
                "audio/x-mpeg",
                "audio/x-mpegurl",
                "audio/x-ms-asf",
                "audio/x-ms-asx",
                "audio/x-ms-wax",
                "audio/x-pn-aiff",
                "audio/x-pn-au",
                "audio/x-pn-realaudio",
                "audio/x-pn-realaudio-plugin",
                "audio/x-pn-wav",
                "audio/x-pn-windows-acm",
                "audio/x-real-audio",
                "audio/x-scpls",
                "audio/x-vorbis+ogg",
                "audio/x-wav",
                "audio/x-flac",
                "application/x-extension-mp4",
                "application/x-flac",
                "application/x-matroska",
                "application/x-shockwave-flash",
                "application/x-flash-video",
                "x-content/audio-cdda",
                "x-content/audio-player",
                "x-content/video-dvd",
                "x-content/video-svcd",
                "x-content/video-vcd",
                "application/ogg"
            ],
            "web_browser": [
                "x-scheme-handler/https",
                "x-scheme-handler/http",
                "x-scheme-handler/ftp",
                "x-scheme-handler/mailto"
            ]
        }
        self.apps = {
            "file_manager": {
                "pcmanfm": PCManFM(),
                "thunar": Thunar()
            },
            "document_reader": {
                "zathura": Zathura(),
                "atril": Atril()
            },
            "image_viewer": {
                "ristretto": Ristretto(),
                "imv": Imv()
            },
            "media_player": {
                "mpv": Mpv(),
                "vlc": Vlc()
            },
            "web_browser": {
                "zen-browser": Zen(),
                "firefox": Firefox()
            }
        }

    def install_all(self):
        for category in self.apps:
            current = self._config.current[category]
            self.apps[category][current].install()

    def change(self, category, app):
        from lib.utils.misc import prompt_y_n
        if app not in self.apps[category]:
            print(f"Error: app '{app}' not found in category '{category}'")
            exit(1)
        if prompt_y_n(f"Set '{app}' as default app for category '{category}'?") == False:
            exit(0)
        current = self._config.current[category]
        if current != app:
            if prompt_y_n(f"Uninstall '{current}'?") == True:
                self.apps[category][current].uninstall()
        self.apps[category][app].install()
        self._config.change(category, app)
        self.configure()
        print(f"Set '{app}' as default for '{category}'")

    def configure(self):
        ml = "[Default Applications]"
        for category in self.associations:
            current = self._config.current[category]
            desktop_file = self.apps[category][current].desktop_file
            for mimetype in self.associations[category]:
                ml += f"\n{mimetype}={desktop_file}"
        with open(f"{environ["CONFIG_DIR"]}/mimeapps.list", "w") as f:
            f.write(ml)
