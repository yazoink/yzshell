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

function configure_fonts() {
    [ ! -d "${HOME}/.fonts" ] && mkdir -p "${HOME}/.fonts"
    cp -rf "./static/.fonts/"* "${HOME}/.fonts"
    echo "Copied fonts"
    fc-cache -fv &> /dev/null
}


function configure_gtk() {
    [ ! -d "${HOME}/.themes" ] && mkdir -p "${HOME}/.themes"
    cp -rf "./static/.themes/"* "${HOME}/.themes"
    gsettings set org.gnome.desktop.interface gtk-theme adw-gtk3
    echo "Copied GTK themes"
}

function configure_icons() {
    [ ! -d "${HOME}/.icons" ] && mkdir -p "${HOME}/.icons"
    cp -rf "./static/.icons/"* "${HOME}/.icons"
    gsettings set org.gnome.desktop.interface cursor-theme BreezeX-Light
    echo "Copied icon themes"
}

function configure_zsh() {
    # oh-my-zsh
    [ ! -d "${HOME}/.oh-my-zsh" ] \
        && sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
    # autosuggestions
    [ ! -d "${HOME}/.oh-my-zsh/plugins/zsh-autosuggestions" ] \
        && git clone https://github.com/zsh-users/zsh-autosuggestions "${HOME}/.oh-my-zsh/plugins/zsh-autosuggestions"
    # syntax highlighting
    [ ! -d "${HOME}/.oh-my-zsh/plugins/zsh-syntax-highlighting" ] \
        && git clone https://github.com/zsh-users/zsh-syntax-highlighting.git "${HOME}/.oh-my-zsh/plugins/zsh-syntax-highlighting"

    [[ "$SHELL" != *"zsh"* ]] \
        && chsh -s "$(which zsh)"
}

function install_executable() {
    sudo install -Dm755 "./bin/yzshell" "/usr/bin/yzshell"
    echo "Installed 'yzshell' to '/usr/bin'"
}

function configure_fstrim() {
    [ ! -d "/etc/cron.weekly" ] && sudo mkdir -p "/etc/cron.weekly"
    [ ! -f "/etc/cron.weekly/fstrim" ] && echo "#!/bin/sh
    fstrim /" | sudo tee /etc/cron.weekly/fstrim >/dev/null
    sudo chmod u+x /etc/cron.weekly/fstrim
}

function install_networkmanager() {
    if ! ls /var/service | grep -q "NetworkManager"; then
        deactivate_service "wpa_supplicant"
        deactivate_service "dhcpcd"
        activate_service "NetworkManager"
        user="$(whoami)"
        sudo usermod -aG network "$user"
        newgrp network
    fi
}

function configure_pipewire() {
    if [ ! -d "/etc/pipewire/pipewire.conf.d" ]; then
        mkdir -p /etc/pipewire/pipewire.conf.d
    fi
    sudo ln -sf /usr/share/examples/wireplumber/10-wireplumber.conf /etc/pipewire/pipewire.conf.d/
}

function install_package() {
    p="$1"
    if ! xbps-query -l | grep -q "ii ${p}-[0-9]"; then
        echo "Installing dependency '${p}'..."
        sudo xbps-install -y "$p"
        echo "Dependency '${p}' installed"
    fi
}

function install_deps() {
    deps=(
        "labwc"
        "labwc-menu-generator"
        "xorg-server-xwayland"
        "noto-fonts-ttf"
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
        "xz"
        "p7zip"
        "zip"
        "unzip"
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
        "vscode"
        "playerctl"
        "xdg-desktop-portal-gtk"
        "xdg-desktop-portal-wlr"
        "xdg-utils"
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
        "zsh"
        "zsh-completions"
        "eza"
        "cryptsetup"
        "gvfs"
        "gvfs-mtp"
        "gvfs-cdda"
        "gvfs-smb"
        "udisks2"
        "mtpfs"
        "ntfs-3g"
        "ffmpeg"
        "yt-dlp"
        "gnome-keyring"
        "fastfetch"
        "mesa-dri"
    )

    for d in "${deps[@]}"; do
        install_package "$d"
    done

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
}

function install_intel_legacy_drivers() {
    deps=(
        "linux-firmware-intel"
        "libva-intel-driver"
        "libvdpau-va-gl"
        "xf86-video-intel"
    )
    for d in "${deps[@]}"; do
        install_package "$d"
    done
    echo "LIBVA_DRIVER_NAME=i965
VDPAU_DRIVER=va_gl" | sudo tee /etc/environment >/dev/null
}

function install_intel_drivers() {
    deps=(
        "linux-firmware-intel"
        "intel-media-driver"
        "libvdpau-va-gl"
        "vulkan-loader"
    )
    for d in "${deps[@]}"; do
        install_package "$d"
    done
    echo "LIBVA_DRIVER_NAME=iHD
VDPAU_DRIVER=va_gl" | sudo tee /etc/environment >/dev/null
}

function install_amd_drivers() {
    deps=(
        "linux-firmware-amd"
        "vulkan-loader"
        "mesa-vulkan-radeon"
        "xf86-video-amdgpu"
        "mesa-vaapi"
        "libvdpau-va-gl"
    )
    for d in "${deps[@]}"; do
        install_package "$d"
    done
    echo "LIBVA_DRIVER_NAME=radeonsi
VDPAU_DRIVER=va_gl" | sudo tee /etc/environment >/dev/null
}

function install_graphics_drivers() {
    gpu=""
    echo "0. None
1. Intel
2. Intel (legacy)
3. AMD"
    while true; do
        read -p "Select graphics card (0-3): " gpu
        [[ "$gpu" =~ [0-3] ]] && break
    done
    case "$gpu" in
        "1") install_intel_drivers & ;;
        "2") install_intel_legacy_drivers & ;;
        "3") install_amd_drivers & ;;
    esac
}

# ensure script run as user
if [ "$EUID" -eq 0 ]; then
    echo "Please do not run as root"
    exit 1
fi

refresh=1
update=1
for a in "$@"; do
    case "$a" in
        "--refresh" | "-r") refresh=0 ;; # refresh configs, don't do full setup
        "--update" | "-u") update=0 ;; # pull update from github
    esac
done

[ $update -eq 0 ] && git pull

# copy data
[ -d "$DATA_DIR" ] && rm -rf "$DATA_DIR"
mkdir -p "$DATA_DIR"

cp -rf "./templates" "${DATA_DIR}/templates" &
cp -rf "./colourschemes" "${DATA_DIR}/colourschemes" &
cp -rf "./assets" "${DATA_DIR}/assets" &
cp -rf "./static" "${DATA_DIR}/static" &
cp -rf "./src" "${DATA_DIR}/src" &

# full setup
if [ $refresh -eq 1 ]; then
    install_deps
    install_graphics_drivers
    yzshell default_apps install_all &
    activate_service "dbus" &
    activate_service "avahi-daemon" &
    activate_service "cupsd" &
    activate_service "elogind" &
    activate_service "bluetoothd" &
    configure_fonts &
    configure_gtk &
    configure_icons &
    configure_zsh &
    configure_pipewire &
    configure_fstrim &
    install_networkmanager &
    install_executable &
fi

yzshell reconfigure

echo "Install Vencord after first discord launch: 'sh -c \"\$(curl -sS https://vencord.dev/install.sh)\"'"
echo "Installation complete!"
