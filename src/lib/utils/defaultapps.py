import subprocess
from sys import exit
from lib.utils.config import Config
from os import environ

class DefaultApps:
    def __init__(self, config=Config()):
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
            ]
        }
        self.available_apps = {
            "file_manager": {
                "pcmanfm": {
                    "desktop_file": "pcmanfm.desktop",
                    "packages": [
                        "pcmanfm",
                        "file-roller",
                        "tumbler",
                        "ffmpegthumbnailer",
                    ]
                },
                "thunar": {
                    "desktop_file": "thunar.desktop",
                    "packages": [
                        "Thunar",
                        "thunar-archive-plugin",
                        "thunar-media-tags-plugin",
                        "thunar-volman",
                        "file-roller",
                        "tumbler",
                        "ffmpegthumbnailer",
                    ]
                }
            },
            "document_reader": {
                "zathura": {
                    "desktop_file": "org.pwmt.zathura.desktop",
                    "packages": [
                        "zathura",
                        "zathura-cb",
                        "zathura-djvu",
                        "zathura-pdf-mupdf",
                        "zathura-ps",
                    ]
                },
                "atril": {
                    "desktop_file": "atril.desktop",
                    "packages": ["atril"]
                }
            },
            "image_viewer": {
                "ristretto": {
                    "desktop_file": "org.xfce.ristretto.desktop",
                    "packages": ["ristretto"]
                },
                "imv": {
                    "desktop_file": "imv.desktop",
                    "packages": ["imv"]
                },
                "imv-dir": {
                    "desktop_file": "imv-dir.desktop",
                    "packages": ["imv"]
                }
            },
            "media_player": {
                "mpv": {
                    "desktop_file": "mpv.desktop",
                    "packages": ["mpv"]
                },
                "vlc": {
                    "desktop_file": "vlc.desktop",
                    "packages": ["vlc"]
                }
            }
        }

    def clean_packages(self):
        pkgs = []
        for a in self.available_apps:
            # a: app category
            # b: app name
            selected = self._config.current[a]
            for b in self.available_apps[a]:
                if b != selected:
                    for c in self.available_apps[a][b]["packages"]:
                        if c not in self.available_apps[a][selected]["packages"]:
                            pkgs.append(c)
        for p in pkgs:
            self._remove_package(p)

    def _install_package(self, p):
        r = subprocess.run(
            f"xbps-query -l | grep -q \"ii {p}-[0-9]\"",
            shell=True,
            capture_output=True,
        ).returncode
        if r != 0:
            print(f"Installing package {p}...")
            subprocess.run(
                f"sudo xbps-install {p}",
                shell=True
            )
            print(f"Installed package {p}...")

    def _remove_package(self, p):
        r = subprocess.run(
            f"xbps-query -l | grep -q \"ii {p}-[0-9]\"",
            shell=True,
            capture_output=True,
        ).returncode
        if r == 0:
            print(f"Removing package {p}...")
            subprocess.run(
                f"sudo xbps-remove -o {p}",
                shell=True
            )
            print(f"Removing package {p}...")

    def install_packages(self):
        pkgs = []
        for a in self.available_apps:
            selected = self._config.current[a]
            pkgs += self.available_apps[a][selected]["packages"]
        for p in pkgs:
            self._install_package(p)

    def write_mimeapps_list(self):
        ml = "[Default Applications]"
        for a in self.associations:
            selected = self._config.current[a]
            desktop_file = self.available_apps[a][selected]["desktop_file"]
            associations = self.associations[a]
            for b in associations:
                ml += f"\n{b}={desktop_file}"
        with open(f"{environ["CONFIG_DIR"]}/mimeapps.list", "w") as f:
            f.write(ml)
        print("Default apps configured")