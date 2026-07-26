#!/usr/bin/env bash

export XBPS_DISTDIR="$HOME/.void-packages"

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
    "labwc-menu-generator"
    "xorg-server-xwayland"
    "noto-fonts-ttf"
    "nerd-fonts"
    "noto-fonts-emoji"
    "foot"
    "yazi" 
    "qt5-wayland"
    "qt6-wayland"
    "qt5ct" 
    "qt6ct" 
    "kvantum" 
    "eww"
    "git"
    "make"
    "ripgrep"
    "xtools"
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
    "python3-BeautifulSoup4"
    "python3-lxml"
    "python3-requests"
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
    "network-manager-applet"
    "wayland-pipewire-idle-inhibit"
    "NetworkManager"
    "pavucontrol-qt"
    "cups"
    "cups-filters"
    "gutenprint"
    "system-config-printer"
    "nss-mdns"
    "avahi"
    "poweralertd"
    "polkit"
    "mate-polkit"
    "bluez"
    "libspa-bluetooth"
    "blueman"
    "pipewire"
    "wireplumber"
    "alsa-utils"
    "pulseaudio-utils"
    "alsa-pipewire"
    "libjack-pipewire"
    "mesa-dri"
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
activate_service "bluetoothd"

# fstrim
[ ! -d "/etc/cron.weekly" ] && sudo mkdir -p "/etc/cron.weekly"
echo "#!/bin/sh
fstrim /" | sudo tee /etc/cron.weekly/fstrim

sudo chmod u+x /etc/cron.weekly/fstrim

if ! ls /var/service | grep -q "NetworkManager"; then
    deactivate_service "wpa_supplicant"
    deactivate_service "dhcpcd"
    activate_service "NetworkManager"
    user="$(whoami)"
    sudo usermod -aG network "$user"
    newgrp network
fi

if [ ! -d "/etc/pipewire/pipewire.conf.d" ]; then
    mkdir -p /etc/pipewire/pipewire.conf.d
fi
sudo ln -sf /usr/share/examples/wireplumber/10-wireplumber.conf /etc/pipewire/pipewire.conf.d/

# install vpsm
if [ ! -d "${HOME}/.void-packages" ]; then
    git clone https://github.com/void-linux/void-packages.git ~/.void-packages
    echo "XBPS_ALLOW_RESTRICTED=yes" >> ~/.void-packages/etc/conf
    git clone https://github.com/sinetoami/vpsm.git ~/.local/share/vpsm
    (
        cd ~/.local/share/vpsm || exit
        sudo make install
    )
fi


vpsm_deps=("discord")

for d in "${vpsm_deps[@]}"; do
    if ! xbps-query -l | grep -q "ii ${d}-[0-9]"; then
        echo "Installing dependency '${d}'..."
        vpsm install "$d"
        echo "Dependency '${d}' installed"
    fi
done

# install executables
sudo install -Dm755 "./bin/yzshell" "/usr/bin/yzshell"
echo "Installed 'yzshell' to '/usr/bin'"

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
configure_icons=0
for a in "$@"; do
    case "$a" in
        "--dont-configure-fonts" | "-df") configure_fonts=1;;
        "--dont-configure-gtk" | "-dg") configure_gtk=1;;
        "--dont-configure-icons" | "-di") configure_icons=1;;
    esac
done

if [ $configure_gtk -eq 0 ]; then
    [ ! -d "${HOME}/.themes" ] && mkdir -p "${HOME}/.themes"
    cp -rf "./static/.themes/"* "${HOME}/.themes"
    gsettings set org.gnome.desktop.interface gtk-theme adw-gtk3
    echo "Copied GTK themes"
fi

if [ $configure_icons -eq 0 ]; then
    [ ! -d "${HOME}/.icons" ] && mkdir -p "${HOME}/.icons"
    cp -rf "./static/.icons/"* "${HOME}/.icons"
    gsettings set org.gnome.desktop.interface cursor-theme BreezeX-Light
    echo "Copied icon themes"
fi

if [ $configure_fonts -eq 0 ]; then
    [ ! -d "${HOME}/.fonts" ] && mkdir -p "${HOME}/.fonts"
    cp -rf "./static/.fonts/"* "${HOME}/.fonts"
    echo "Copied fonts"
    fc-cache -fv &> /dev/null
fi

yzshell reconfigure
yzshell default_apps install_all

echo "Install Vencord after first discord launch: 'sh -c \"\$(curl -sS https://vencord.dev/install.sh)\"'"

echo "Installation complete!"