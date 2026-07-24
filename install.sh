#!/usr/bin/env bash

DATA_DIR="${HOME}/.local/share/yzshell"

deps=(
    "labwc"
    "foot"
    "yazi" 
    "qt5ct" 
    "qt6ct" 
    "kvantum" 
    "eww"
    "dbus"
    "jq"
    "curl"
    "lm_sensors"
    "mako"
    "libnotify"
    "mako"
    "Waybar"
    "font-awesome6"
    "wtype"
    "hyprpicker"
    "wl-clipboard"
    "grim"
    "slurp"
    "swaybg"
    "python"
    "python3-gobject"
    "python3-Pillow"
    "xorg-server-xwayland"
    "elogind"
    "gsettings-desktop-schemas"
    "dconf"
    "dconf-editor"
    "psmisc"
    "bc"
    "audacious"
    "keepassxc"
    "playerctl"
    "xdg-desktop-portal-gtk"
    "xdg-desktop-portal-wlr"
    "papirus-icon-theme"
    "papirus-folders"
    "SwayOSD"
    "swayidle"
    "swaylock"
    "wlopm"
)

# activate services
if ! ls /var/service | grep -q "dbus"; then
    sudo ln -s /etc/sv/dbus /var/service
fi

if ! ls /var/service | grep -q "elogind"; then
    sudo ln -s /etc/sv/elogind /var/service
fi

for d in "${deps[@]}"; do
    if ! xbps-query -l | grep -q "ii ${d}-[0-9]"; then
        sudo xbps-install -y "$d"
    fi
done

# install executable
sudo install -Dm755 "./bin/yzshell" "/usr/bin/yzshell"
sudo install -Dm755 "./bin/screenshot" "/usr/bin/screenshot"
sudo install -Dm755 "./bin/toggle_dnd" "/usr/bin/toggle_dnd"
sudo install -Dm755 "./bin/colour_picker" "/usr/bin/colour_picker"

# copy data
[ -d "$DATA_DIR" ] && rm -rf "$DATA_DIR"
mkdir -p "$DATA_DIR"

cp -rf "./templates" "${DATA_DIR}/templates"
cp -rf "./colourschemes" "${DATA_DIR}/colourschemes"
cp -rf "./assets" "${DATA_DIR}/assets"
cp -rf "./static" "${DATA_DIR}/static"
cp -rf "./src" "${DATA_DIR}/src"
cp -rf "./static/.themes" "${HOME}/.themes"
cp -rf "./static/.fonts" "${HOME}/.fonts"

fc-cache -fv

yzshell reconfigure