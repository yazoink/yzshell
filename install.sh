#!/usr/bin/env bash

DATA_DIR="${HOME}/.local/share/yzshell"

function activate_service() {
    if ! ls /etc/sv | grep -q "$1"; then
        echo "Error: service '${1}' not found"
        exit 1
    fi
    if ! ls /var/service | grep -q "$1"; then
        sudo ln -s /etc/sv/"$1" /var/service
        echo "Activated service '${1}'"
    fi
}

function deactivate_service() {
    if ls /var/service | grep -q "$1"; then
        sudo sv down wpa_supplicant
        sudo rm /var/service/"$1"
        echo "Deactivated service '${1}'"
    fi
}

if [ "$EUID" -eq 0 ]; then 
    echo "Please do not run as root"
    exit 1
fi

# install deps
deps=(
    "labwc"
    "foot"
    "yazi" 
    "qt5ct" 
    "qt6ct" 
    "kvantum" 
    "eww"
    "git"
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
    "imv"
    "zathura"
    "wl-clip-persist"
    "nm-tray"
    "wayland-pipewire-idle-inhibit"
    "NetworkManager"
    "pwvucontrol"
    "cups"
    "cups-filters"
    "gutenprint"
    "system-config-printer"
    "nss-mdns"
    "avahi"
)

for d in "${deps[@]}"; do
    if ! xbps-query -l | grep -q "ii ${d}-[0-9]"; then
        echo "Installing dependency '${d}'..."
        sudo xbps-install -y "$d"
        echo "Dependency '${d}' installed"
    fi
done

# activate services
activate_service "dbus"
activate_service "avahi-daemon"
activate_service "cupsd"
activate_service "elogind"

if ! ls /var/service | grep -q "NetworkManager"; then
    deactivate_service "wpa_supplicant"
    deactivate_service "dhcpcd"
    activate_service "NetworkManager"
    user="$(whoami)"
    sudo usermod -aG network "$user"
    newgrp network
fi

# install zen browser
if ! which zen &> /dev/null; then
    echo "Installing zen browser..."
    mkdir -p ~/src
    (
        cd ~/src || exit
        git clone https://github.com/void-linux/void-packages.git
        git clone https://github.com/salastro/zen-browser.git
        cp -rf zen-browser void-packages/srcpkgs/
        cd void-packages || exit
        ./xbps-src binary-bootstrap
        echo XBPS_ALLOW_RESTRICTED=yes >> etc/conf
        ./xbps-src pkg zen-browser
        sudo xbps-install --repository=hostdir/binpkgs zen-browser
    )
    echo "Zen browser installed"
fi

# install executables
sudo install -Dm755 "./bin/yzshell" "/usr/bin/yzshell"
echo "Installed 'yzshell' to '/usr/bin'"
sudo install -Dm755 "./bin/screenshot" "/usr/bin/screenshot"
echo "Installed 'screenshot' to '/usr/bin'"
sudo install -Dm755 "./bin/toggle_dnd" "/usr/bin/toggle_dnd"
echo "Installed 'toggle_dnd' to '/usr/bin'"
sudo install -Dm755 "./bin/colour_picker" "/usr/bin/colour_picker"
echo "Installed 'colour_picker' to '/usr/bin'"

# copy data
[ -d "$DATA_DIR" ] && rm -rf "$DATA_DIR"
mkdir -p "$DATA_DIR"

cp -rf "./templates" "${DATA_DIR}/templates"
cp -rf "./colourschemes" "${DATA_DIR}/colourschemes"
cp -rf "./assets" "${DATA_DIR}/assets"
cp -rf "./static" "${DATA_DIR}/static"
cp -rf "./src" "${DATA_DIR}/src"

echo "Copied data files to '${DATA_DIR}'"

configure_fonts=0
configure_gtk=0
reconfigure=0
for a in "$@"; do
    case "$a" in
        "--dont-configure-fonts" | "-df") configure_fonts=1;;
        "--dont-configure-gtk" | "-dg") configure_gtk=1;;
        "--dont-reconfigure" | "-dr") reconfigure=1;;
    esac
done

if [ $configure_gtk -eq 0 ]; then
    cp -rf "./static/.themes" "${HOME}/.themes"
    echo "Copied GTK themes"
fi

if [ $configure_fonts -eq 0 ]; then
    cp -rf "./static/.fonts" "${HOME}/.fonts"
    echo "Copied fonts"
    fc-cache -fv
fi

if [ $reconfigure -eq 0 ]; then
    yzshell reconfigure
fi

echo "Installation complete!"