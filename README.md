# yzshell

My very messy dotfiles.

These dots are heavily centered around my preferences, but anyone can use them.
A lot of options can be toggled during the installation progress, and more can
be configured with the `yzctl` TUI, or manually with `yzconf`.

Run `yzbinds`, or press Super+B to view the keybinds.

## Showcase

<img width="1366" height="768" alt="fetch+startmenu" src="https://github.com/user-attachments/assets/ac840ed3-7dfc-43fa-a76d-ace28d6012ad" />
<img width="1366" height="768" alt="nvim+htop" src="https://github.com/user-attachments/assets/15f62199-538c-4e8a-b1d7-bcf03db157eb" />

### Start Menu

https://github.com/user-attachments/assets/b0fcd143-e904-4386-93e1-cc85f0444e23

### Settings

https://github.com/user-attachments/assets/a4f55068-4c10-45f9-930e-8e45436ad661

### Calendar

https://github.com/user-attachments/assets/8f12eba6-c3d8-4633-8edc-7b0325386480

### Application Themes

<img width="1366" height="768" alt="gtk" src="https://github.com/user-attachments/assets/66f41eb5-5be3-479d-bbbe-e8f8230890dc" />
<img width="1366" height="768" alt="web" src="https://github.com/user-attachments/assets/142071e2-9229-49dc-80b3-c816957ae1d4" />
<img width="1366" height="768" alt="qt" src="https://github.com/user-attachments/assets/e7403703-4537-4b40-b329-36252bfc1be3" /><img width="1366" height="768" alt="vscode" src="https://github.com/user-attachments/assets/0b1e96fa-e567-4937-a0ea-7e09a582b877" />

### Lockscreen

<img width="1366" height="768" alt="mpv-shot0001" src="https://github.com/user-attachments/assets/78525d97-3a9d-4514-bfa9-7d8829c2a6b5" />

## Software

- Window manager: Hyprland
- Shell: Zsh
- Widgets: EWW
- Run launcher: Wofi
- Notifications: Mako/SwayOSD
- Lockscreen: Hyprlock
- Bar: Waybar
- IDE: VsCodium/Nvim
- Browser: Zen

## Features

- Various application themes/configs (Zen Browser, Neovim, Vscodium, Vesktop, ncmpcpp, etc.)
- Colourscheme and wallpaper switcher
- \>70 colourschemes
- Inbuilt screenshot and screen recording utilities
- Unified theming for GTK 2/3/4 and Qt 5/6
- A bunch of CLI utilities: `yzshell`, `yzctl`, `yzbinds`, `yzconf`, `yzpicker`, `yzrecorder`, `yzshot`, `yzwallpaper`, `yzwidgets`, `base16-to-yzshell-scheme`, and `base16-to-yzshell-template` (run `-h` on them for details)
- Really bad code, but at least it's not vibe-coded

## Installation

Prerequisites:

- Fresh Arch install (I do not recommend installing on a system with any existing
  configs, the installer will backup and override any conflicting files)
- NetworkManager
- Pipewire
- Git
- No AUR helper, or Yay

```bash
git clone https://github.com/yazoink/yzshell
cd yzshell
./install.sh --optional-deps
```

After running the install script, and rebooting, Hyprland will automatically
launch with yzshell. Upon first launching Hyprland, a terminal window will open, which will
install plugins. This will automatically launch every time Hyprland is reloaded
if it is detected that plugins are not installed. To run this manually:
`yzshell-install-hyprland-plugins`.

## Configuration

yzshell is generally configured with the `yzctl` command, which provides
a TUI. The `yzconf` command can also be used for manual configuration
(`yzctl` is just a wrapper for it). Note that when configuring manually, you
need to run `yzconf deploy_configs --refresh`, and then reload the shell
(`yzshell reload` or Ctrl+Shift+R) to apply any changes; otherwise bugs may
occur.

Extra Hyprland configurations (i.e. monitors) can be placed in
`~/.config/yzshell/hyprland-extra.lua`, and extra Neovim configurations can be
placed in `~/.config/yzshell/nvim-extra.lua`.

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
./install.sh --skip-deps
yzshell reload
```

from the repo directory. This will re-copy all the necessary files.

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

## Troubleshooting

### Hyprbars won't work after updating

Try hard resetting hyprpm, and if that doesn't work it's probably a Hyprbars problem.

```
hyprpm purge-cache
yzshell-install-hyprland-plugins
```
