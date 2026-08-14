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

## Screenshots

<img width="1366" height="768" alt="20260807_22:46:23" src="https://github.com/user-attachments/assets/21aed7b9-3430-4573-9449-1fcf0bd9a67c" />

## Installation

Prerequisites:

- Base Arch install
- NetworkManager
- Pipewire
- `git` or `curl`

### With curl

(I haven't fully tested this method, so maybe don't yet)

`bash -c $(curl -Ss https://raw.githubusercontent.com/yazoink/yzshell/refs/heads/main/install.sh --optional-deps)`

### With git

```bash
git clone https://github.com/yazoink/yzshell
cd yzshell
./install.sh --local --optional-deps
```
