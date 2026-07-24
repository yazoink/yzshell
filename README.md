# yzshell

My very messy dotfiles.

Software:
- **OS** - Void
- **Shell** - Zsh
- **Window Manager** - Labwc
- **Bar** - Waybar
- **Widgets** - EWW
- **Notifications** - Mako
- **Terminal** - Foot
- **Browser** - Zen
- **File Manager** - PCManFM (GUI), Yazi (TUI)
- **Application Launcher** - EWW
- **Run Launcher** - Wofi
- **Wallpaper** - Swaybg
- **OSD** - SwayOSD

Additional configurations:
- GTK and Qt themes (customised adw-gtk3 and KvLibadwaita)
- Icons (Papirus)
- Fonts (Gabarito (sans), Aporetic Serif Mono (monospace), TeX Gyre Schola (sans-serif))

Features:
- Colourscheme switcher
- Wallpaper switcher
- Screenshot utility
- Colour picker utility
- Do-not-disturb toggle
- Media, system monitor, and weather widgets

## Showcase

<img width="1359" height="767" alt="20260724_19:05:54_screenshot" src="https://github.com/user-attachments/assets/0234cf5c-3980-4254-aa7c-c7fe08830152" />
<img width="1366" height="766" alt="20260724_19:03:54_screenshot" src="https://github.com/user-attachments/assets/94eb5a97-ddf2-4c46-9014-5cea320a0ccd" />
<img width="1366" height="768" alt="20260724_19:06:10_screenshot" src="https://github.com/user-attachments/assets/92b7ab56-204f-4d5d-9b6c-244284afa6c0" />
<img width="1366" height="767" alt="20260724_19:06:44_screenshot" src="https://github.com/user-attachments/assets/d51d9271-28bd-401a-b0ab-6521737ae672" />
<img width="1366" height="767" alt="20260724_19:06:27_screenshot" src="https://github.com/user-attachments/assets/3f119230-d7b5-4304-9bf2-6cad7148a823" />
<img width="1366" height="767" alt="20260724_19:09:33_screenshot" src="https://github.com/user-attachments/assets/78084ab4-236f-4dce-8768-e961bb03339b" />


## Installation

Prerequisites:
- Base Void installation
- Graphics drivers installed

```bash
git clone https://github.com/yazoink/yzshell
cd yzshell
./install.sh
```

And reboot.

## Configuration

yzshell looks for a config file at `~/.config/yzshell/config.json`. A basic 
config would look as such:

```json
{
  "colourscheme": "mellow",
  "bar_show_battery": true,
  "bar_show_backlight": true,
  "profile_image": "/home/user/.local/share/yzshell/assets/images/profile_image.jpg",
  "screenshot_dir": "/home/user/pic/screenshots",
  "wallpaper_dir": "/home/user/pic",
  "wallpaper_image": "a_painting_of_flowers_and_leaves.jpeg",
  "wallpaper_mode": "fill",
  "zen_profile_dir": "/home/user/.config/zen/gd1z8qc7.Default (release)"
}
```

### Options

#### colourscheme

Value must be the name of a file in `./colourschemes`
(`~/.local/share/yzshell/colourschemes` once installed), omitting the `.json`.

#### bar_show_battery

Whether the status bar should display battery module -- `true` or `false`.

#### bar_show_backlight

Whether the status bar should display backlight module -- `true` or `false`.

#### profile_image

Absolute path to the profile image used by the control panel widget.

#### screenshot_dir

Absolute path of directory to save screenshots.

#### wallpaper_dir

Absolute path to directory containing wallpaper.

#### wallpaper_image

Name of wallpaper file.

#### wallpaper_mode

Wallpaper mode -- `stretch`, `fit`, `fill`, `center`, or `tile`.

#### zen_profile_dir

Absolute path to Zen Browser profile directory.

## TODO
- vencord config/theme
- zen config
- nvim config/theme