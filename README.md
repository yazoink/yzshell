# yzshell

My very messy dotfiles.

## Software

- Window manager: Hyprland
- Terminal: Foot
- Shell: Zsh
- Widgets: EWW
- Run launcher: Wofi
- Notifications: Mako/SwayOSD
- Lockscreen: Hyprlock
- Bar: Waybar
- Browser: Zen
- File manager: Thunar or PCManFM

## Features

- Various application themes/configs (Zen Browser, Neovim, Vscodium, Vesktop, ncmpcpp, etc.)
- Colourscheme and wallpaper switcher
- Inbuilt screenshot and screen recording utilities
- Unified theming for GTK 2/3/4 and Qt 5/6
- A bunch of CLI utilities: `yzshell`, `yzctl`, `yzconf`, `yzpicker`, `yzrecorder`, `yzshot`, `yzwallpaper`, `yzwidgets`, `base16-to-yzshell-scheme`, `base16-to-yzshell-template`, and `zenconf` (run `-h` on them for details)
- Really bad code, but at least it's not vibe-coded

## Keybinds

- Mod + Return: open terminal
- Mod + W: open browser
- Mod + E: open file manager
- Mod + Shift + L: lock screen
- Mod + R: open run launcher
- Mod + P: open start menu
- Mod + Shift + C: toggle calendar widget
- Mod + Shift + Q: toggle power menu
- Mod + Shift + A: toggle shell appearance settings
- Mod + Tab: toggle workspace switcher
- Mod + Shift + R: reload shell
- Mod + Shift + B: reload bar
- Mod + C: pick colour
- Mod + Shift + D: toggle do-not-disturb
- Mod + Shift + I: toggle idle inhibitor
- Mod + Alt + S: toggle screenshot widget
- Mod + S: take selective screenshot
- Mod + Ctrl + S: take full screenshot
- Mod + Q: close active window
- Mod + Ctrl + Q: kill active window
- Mod + X: pin window
- Mod + M: toggle maximise active window
- Mod + Shift + M: toggle fullscreen active window
- Mod + F: toggle float active window
- Mod + \[1-9]: switch to workspace
- Mod + Shift + \[1-9]: move active window to workspace
- Mod + Shift + S: toggle special workspace
- Mod + Ctrl + Up: move active window to special workspace
- Mod + \[Left|Right|Up|Down]: focus in direction
- Mod + Shift + \[Left|Right|Up|Down]: move active window in direction
- Mod + \[-|=]: increase/decrease split ratio
- Mod + K: swap split

### Widgets

#### Start menu

- \[Up|Down]: select app
- Return: open selected app, or close if none selected
- Esc: close

#### Calendar

- Esc: close

#### Power Menu

- L: lock screen
- S: shut down
- R: reboot
- E: exit desktop
- Esc: close

#### Screenshot

- Esc: close

#### Appearance settings

- Esc: close

#### Workspace switcher

- \[Left|Right|Up|Down]: switch to next/prev workspace
- \[1-9]: switch to workspace and close
- \[Esc|Tab|Return]: close

## Screenshots

<img width="1366" height="768" alt="20260807_22:46:23" src="https://github.com/user-attachments/assets/21aed7b9-3430-4573-9449-1fcf0bd9a67c" />
<img width="1366" height="768" alt="20260815_11:09:20" src="https://github.com/user-attachments/assets/fb96b68f-5c1d-49d2-ab51-5f64bb32096d" />
<img width="1366" height="768" alt="20260815_18:58:47" src="https://github.com/user-attachments/assets/dbf5045b-3a65-4b1e-9bab-45ab979ec7d7" />
<img width="1366" height="768" alt="20260815_19:01:23" src="https://github.com/user-attachments/assets/ce07f2ef-582b-4d08-98e9-ab6a6c3a74e1" />
<img width="2560" height="1440" alt="20260818_23:53:57" src="https://github.com/user-attachments/assets/9648a396-0136-409a-8a05-0140964df86e" />
<img width="2560" height="1440" alt="20260818_23:52:05" src="https://github.com/user-attachments/assets/0c4a99de-13ac-46ae-9b3e-d90a079aa4f2" />
<img width="2560" height="1440" alt="20260818_23:54:23" src="https://github.com/user-attachments/assets/ae5d7180-53a5-4e4a-ba4a-bc671fe5e10c" />
<img width="2560" height="1440" alt="20260818_23:50:46" src="https://github.com/user-attachments/assets/06829364-4664-47d7-957c-715ee9166569" />
<img width="2560" height="1440" alt="20260818_23:51:11" src="https://github.com/user-attachments/assets/728c8c49-7ee5-4a58-b271-aa63a7bfe8cc" />
<img width="546" height="85" alt="20260814_20:50:35" src="https://github.com/user-attachments/assets/e8b43321-1925-4424-b53c-be088c30c8c5" />
<img width="641" height="568" alt="20260902_23:30:32" src="https://github.com/user-attachments/assets/b3f80f9d-6d56-4c54-8cec-9e6d1cd6dea3" />

## Installation

These dots are heavily centered around my preferences, but anyone can use them.
A lot of options can be toggled during the installation progress, and more can
be configured with the `yzctl` TUI, or manually with `yzconf`.

Note: upon first launching Hyprland, a terminal window will open, which will
install plugins. This will automatically launch every time Hyprland is reloaded
if it is detected that plugins are not installed. To run this manually:
`yzshell-install-hyprland-plugins`.

Prerequisites:

- Base Arch install (I do not recommend installing on a system with any existing configs, it will just override some stuff, and also stow will complain)
- NetworkManager
- Pipewire
- `gum`
- `git` or `curl`

### With curl

`bash -c "$(curl -Ss https://raw.githubusercontent.com/yazoink/yzshell/refs/heads/main/install.sh)" "" --optional-deps`

### With git

```bash
git clone https://github.com/yazoink/yzshell
cd yzshell
./install.sh --local --optional-deps
```

## Updating

### With curl

Run the install command again.

### With git

Run `git pull` on the repo and run the install command again.

## Configuration

yzshell is generally configured with the `yzctl` command, which provides
a TUI. The `yzconf` command can also be used for manual configuration
(`yzctl` is just a wrapper for it). Note that when configuring manually, you
need to run `yzconf deploy_configs --refresh`, and then reload the shell
(`yzshell reload` or Ctrl+Shift+R) to apply any changes; otherwise bugs may
occur.

### Default terminal / file manager / web browser

The default terminal / file manager / web browser are declared with the options:
`terminal`, `file_manager`, and `web_browser`, and they should be set to the
launch command of the application.

### Fonts

Fonts are configured with the options: `sans_font`, `mono_font`, `serif_font`,
and `terminal_font_size`. If configuring manually, run `fc-cache -fv` after
changing any of the first three.

### Misc. notable options

- Show/hide the battery/backlight modules on the bar: `bar_show_battery`,
  `bar_show_backlight`.
- Profile image: `profile_image`.
- Screenshot / screen recording directories: `screenshot_dir`, `recording_dir`.
- Music directory for MPD: `music_dir`.
- oh-my-zsh theme: `oh_my_zsh_theme`.
- Papirus-Folders colour: `papirus_folders_colour`
- Touchpad scrolling sensitivity: `touchpad_scroll_factor`.

## Further customisation

Aside from the config options, there is no way to override the yzshell dotfiles,
or add custom colourschemes or templates, aside from forking the repo. I don't
intend to change this anytime soon unless other people actually start using
this.

Nonetheless, if you want to fork the repo, it's pretty easy to change basic
stuff.

To apply any changes, run:

```bash
./install.sh --local --no-deps
yzshell reload
```

from the root directory. This will re-copy all the necessary files.

### Colourschemes

yzshell uses its own colourscheme format, similar to base16, and written in
json. A template can be found at `misc/colourscheme-template.json`. A complete
scheme file would look as such:

```json
{
  "scheme": "Carob",
  "author": "yazoink (https://github.com/yazoink/carob-theme)",
  "polarity": "dark",
  "background": "242120",
  "foreground": "C8BAA4",
  "red": "C65F5F",
  "orange": "d08b65",
  "yellow": "d9b27c",
  "green": "859e82",
  "cyan": "829e9b",
  "blue": "728797",
  "purple": "998396",
  "brown": "ab9382"
}
```

The yzshell format doesn't include background highlights because they get
generated automatically during the template-building process. It doesn't
include foreground highlights either because I don't really like them.

To add a scheme, place it in `colourschemes/`, and it will be detected
automatically (same goes for removals and modifications). The name of the file
(minus the `.json`) will be used as the scheme's ID.

The `base16-to-yzshell-scheme` script can be used to convert
base16 yaml themes to the yzshell format:

`base16-to-yzshell-theme --source base16-theme.yaml --polarity light`

The colours of the titlebar buttons can be specified by adding:
`"window_buttons": ["red", "orange", "yellow"]` -- the default is
`["red", "yellow", "green"]`.

The accent colour can be specified by adding `"accent": "purple"` -- defaults
to `"blue"`.

### Dotfiles

All static dotfiles can be found in `dotfiles/`. All files in this directory
get copied to `~/.dotfiles` and symlinked with stow as-is.

There are some other configs which are modified during the deployment process
in `misc/`.

#### Templates

yzshell uses Mustache templates for most dynamically generated configs.
The tags used in building the templates contain all yzshell configuration
options, all colourscheme values, plus a few extras. To view all of the
available tags, run `yzconf dump_mustache_data`.

The colourscheme tags consist of all values declared in json, plus `surface1`,
`surface2`, `surface3`, and `surface4` (equivalent to base\[1-4]), and
`window_button1`, `window_button2`, and `window_button3` (titlebar buttons).
`accent` is converted from the name of its colour to the colour itself, and the
tags `<COL>-rgb-r`, `<COL>-rgb-g`, `<COL>-rgb-b`, `<COL>-hex`, and
`<COL>-hex-bgr` are also included.

The `base16-to-yzshell-template` script can be used to convert
base16 templates to yzshell templates:

`base16-to-yzshell-template --source template.mustache`

To add a template to yzshell, copy it to `templates/`, and add it to
`templates/templates.json`:

```json
{
    ...
    "<TEMPLATE>": "<DESTINATION>"
}
```

Or for multiple destinations:

```json
{
    ...
    "<TEMPLATE>": [
        "<DESTINATION 1>",
        "<DESTINATION 2>"
    ]
}
```
