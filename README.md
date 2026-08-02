# yzshell

My very messy dotfiles.

Software:
- **OS** - Arch
- **Shell** - Zsh
- **Window Manager** - Hyprland/Labwc
- **Bar** - Waybar
- **Widgets** - EWW
- **Notifications** - Mako
- **Application Launcher** - EWW
- **Run Launcher** - Wofi
- **Wallpaper** - Swaybg
- **OSD** - SwayOSD
- **Lockscreen** - Hyprlock

Features:
- Extensive CLI interface
- Custom GTK and Qt themes
- Colourscheme switcher
- Wallpaper switcher
- Screenshot utility
- Colour picker utility
- Do-not-disturb toggle
- Media, system monitor, and weather widgets

## Showcase

### Hyprland

<img width="1359" height="767" src="/assets/images/screenshots/hyprland-1.png" />
<img width="1359" height="767" src="/assets/images/screenshots/hyprland-2.png" />
<img width="1359" height="767" src="/assets/images/screenshots/hyprland-3.png" />

### Labwc

<img width="1359" height="767" src="/assets/images/screenshots/labwc-1.png" />
<img width="1359" height="767" src="/assets/images/screenshots/labwc-2.png" />

### Misc

<img width="1359" height="767" src="/assets/images/screenshots/logout.png" />
<img width="1359" height="767" src="/assets/images/screenshots/colourschemes.png" />
<img width="1359" height="767" src="/assets/images/screenshots/lockscreen.png" />

## Installation

Prerequisites:
- Base Arch installation with git installed
- Internet connection

```
$ git clone https://github.com/yazoink/yzshell
$ cd yzshell
$ ./install.sh
```

And reboot.      

The script will prompt the selection of the window manager, and also the 
installation of graphics drivers (on particular hardware).

### Updating

```
$ cd yzshell
$ ./install.sh -u
```

## Configuration

yzshell looks for a config file at `~/.config/yzshell/config.json`. A basic 
config would look as such:

```json
{
    "window_manager": "hyprland",
    "colourscheme": "moonfly",
    "bar_show_battery": true,
    "bar_show_backlight": true,
    "profile_image": "/home/gene/.local/share/yzshell/assets/images/profile_image.jpg",
    "screenshot_dir": "/home/gene/pic/screenshots",
    "wallpaper_dir": "/home/gene/pic/wallpapers",
    "wallpaper_image": "andrei-lazarev-QtM-8j_1o3Q.jpg",
    "wallpaper_mode": "fill",
    "zen_profile_dir": "/home/gene/.config/zen/htooy43a.Default (release)",
    "file_manager": "pcmanfm",
    "web_browser": "zen-browser",
    "document_reader": "zathura",
    "terminal": "foot",
    "media_player": "mpv",
    "image_viewer": "imv",
    "run_launcher": "wofi --show run",
    "labwc_desktops": 9,
    "touchpad_scroll_factor": 0.15,
    "oh_my_zsh_theme": "robbyrussell",
    "enable_h264ify": false,
    "papirus_folders_colour": "palebrown"
}
```

Note: it's always a good idea to run `yzshell reconfigure` after updating.
Things may break if you don't.

### Options

#### window_manager

Declares the window manager yzshell uses. Do not edit this option manually.

#### colourscheme

Declares the desktop colourscheme. Not recommended to edit manually.

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

#### file_manager / web_browser / media_player / image_viewer / document_reader

Declares default apps. Do not edit manually

#### terminal / run_launcher

Declares the commands to run the terminal / run launcher. The only apps
that are actually configured/installed are `foot` and `wofi`. Overrides are not
a big deal with these, however.

#### labwc_desktops

Number of workspaces / virtual desktops Labwc configures. Any number over 9
will probably not work properly.

#### touchpad_scroll_factor

Sets the scrolling sensitivity for the touchpad.

#### oh_my_zsh_theme

[One of these](https://github.com/ohmyzsh/ohmyzsh/wiki/Themes).

#### enable_h264ify

Enable the h264ify browser extension 
(only works for Zen right now because I'm lazy). Accepts `true` or `false`.

### papirus_folders_colour

Colour for the icon theme's folders. Run `papirus-folders -l` for options.

## CLI Interface

yzshell provides a cli interface for launching and interacting with different
desktop components.      

The `yzshell` command, on its own, will restart/launch the shell. Hyprland and
Labwc are configured to launch it automatically.

### Configuration

yshell's config file can be edited manually, or with 
`yzshell config set <option> <value>`. Note that `yzshell reconfigure` still
needs to be run manually after updating.      

To get the value of a config option, you can also run 
`yzshell config get <option>`.

### Reconfiguration

When the config is updated, `yzshell reconfigure` must be run to apply the 
changes, or else bugs may occur. This command re-generates all of the
application config files according to the options in yzshell's config file.

### Colourscheme

To change the colourscheme, run `yzshell colourscheme <colourscheme>`. To list
available schemes, run `yzshell colourscheme list`.

### Default Apps

yzshell installs and configures default apps for a number of categories 
(i.e. web browser, file manager...). To list the available categories, run
`yzshell default_apps get categories`. To list the apps available in a 
category, run `yzshell default_apps get apps <category>`.

To change a default app, run `yzshell default_apps set <category> <app>`. The
configurations and dependencies will be handled automatically.

### Window Manager

To change the window manager yzshell uses, run 
`yzshell window_manager set <window manager>`. The available options are 
`hyprland` (recommended), and `labwc`.

yzshell also provides a command to cleanly exit the window manager with
`yzshell window_manager exit`.

### Wallpaper

The wallpaper can be set with `yzshell set_wallpaper <path>`.
The wallpaper mode can be set with `yzshell set_wallpaper_mode <mode>`.

### Opening/Closing Widgets

Widgets can be opened/closed/toggled as such:
```
$ yzshell open <widget>
$ yzshell close <widget>
$ yzshell toggle <widget>
$ yzshell close_all_widgets
```

The available widgets are: `calendar`, `control_center`, `power`, 
`screenshot`, and `settings`.

### Misc.

Lock screen: `yzshell lock`.      
Open colour picker: `yzshell pick_colour`.      
Toggle do-not-disturb: `yzshell toggle_dnd`.      

#### Screenshot Utility

Basic usage: `yzshell screenshot` -- takes a fullscreen screenshot and outputs
to the directory specified under `screenshot_dir` in the config file.

Flags:

- `--mode` or `-m`: specifies the mode, accepts `full` or `select` as an 
  argument.
- `--output` or `-o`: specifies the path to save the screenshot.
- `--sleep-time` or `-s`: time in seconds to wait before taking screenshot.


## TODO
- Nvim config/theme
- VSCode config
- Tmux config/theme
- Add more colourschemes
- Add option to change default music player