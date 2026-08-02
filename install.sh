#!/usr/bin/env bash

DATA_DIR="${HOME}/.local/share/yzshell"

function package_installed() {
    pacman -Qi "$1" > /dev/null 2>&1
    return $?
}

function install_package() {
    package_installed "$1"
    if [ $? -ne 0 ]; then
        sudo pacman -S -y --needed "$1"
        exit_if_failed $? "failed to install package '${1}'"
    else
        echo ">> Package '${1}' already installed, skipping..."
    fi
}

function exit_if_failed() {
    ret=$1
    error_msg="$2"
    if [ $ret -ne 0 ]; then
        echo "Error: ${error_msg}"
        exit 1
    fi
}

function install_aur_package() {
    package_installed "$1"
    if [ $? -ne 0 ]; then
        yay -S --needed --norebuild --noredownload "$1"
        exit_if_failed $? "failed to install package '${1}'"
    fi
}

function configure_zsh() {
    # oh-my-zsh
    if [ ! -d "${HOME}/.oh-my-zsh" ]; then
        sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
        exit_if_failed $? "failed to download oh-my-zsh"
        # autosuggestions
        [ ! -d "${HOME}/.oh-my-zsh/plugins/zsh-autosuggestions" ] \
            && git clone https://github.com/zsh-users/zsh-autosuggestions "${HOME}/.oh-my-zsh/plugins/zsh-autosuggestions"
        exit_if_failed $? "failed to download zsh-autosuggestions"
        # syntax highlighting
        [ ! -d "${HOME}/.oh-my-zsh/plugins/zsh-syntax-highlighting" ] \
            && git clone https://github.com/zsh-users/zsh-syntax-highlighting.git "${HOME}/.oh-my-zsh/plugins/zsh-syntax-highlighting"
        exit_if_failed $? "failed to download zsh-syntax-highlighting"
    fi
}

function install_executable() {
    sudo install -Dm755 "./bin/yzshell" "/usr/bin/yzshell"
    echo "Installed 'yzshell' to '/usr/bin'"
}

function install_yay() {
    package_installed "yay"
    if [ $? -ne 0 ]; then
        sudo pacman -S -y --needed base-devel git
        mkdir ~/src
        git clone https://aur.archlinux.org/yay.git ~/src/yay
        exit_if_failed $? "failed to download yay"
        (
            cd ~/src/yay || exit 1
            makepkg -si
            exit_if_failed $? "failed to install yay"
        )
    fi
}

function install_optional_deps() {
    deps=(
        "code"
        "fastfetch"
        "gimp"
        "htop"
        "fastfetch"
        "galculator"
    )
    for d in "${deps[@]}"; do
        install_package "$d"
    done

    aur_deps=(
        "vesktop-bin"
    )

    for d in "${aur_deps[@]}"; do
        install_aur_package "$d"
    done
}

function install_deps() {
    deps=(
        "base-devel"
        "git"
        "freetype2"
        "foot"
        "vim"
        "yazi"
        "qt5-wayland"
        "qt6-wayland"
        "qt5ct"
        "qt6ct"
        "kvantum"
        "direnv"
        "xorg-xwayland"
        "polkit"
        "jq"
        "curl"
        "wget"
        "xz"
        "p7zip"
        "lm_sensors"
        "mako"
        "libnotify"
        "waybar"
        "otf-font-awesome"
        "tex-gyre-fonts"
        "hyprpicker"
        "wl-clipboard"
        "grim"
        "slurp"
        "swaybg"
        "python"
        "python-gobject"
        "python-pillow"
        "python-beautifulsoup4"
        "python-lxml"
        "python-requests"
        "gsettings-desktop-schemas"
        "dconf"
        "psmisc"
        "bc"
        "audacious"
        "playerctl"
        "xdg-desktop-portal-gtk"
        "xdg-desktop-portal-wlr"
        "xdg-utils"
        "papirus-icon-theme"
        "swayosd"
        "swayidle"
        "hyprlock"
        "network-manager-applet"
        "pavucontrol"
        "zsh"
        "zsh-completions"
        "eza"
        "gnome-keyring"
        "adw-gtk-theme"
        "man-db"
        "gvfs"
        "gvfs-smb"
        "gvfs-mtp"
        "gvfs-gphoto2"
        "udisks2"
    )

    for d in "${deps[@]}"; do
        install_package "$d"
    done

    curl -sS https://github.com/elkowar.gpg | gpg --import -i -
    curl -sS https://github.com/web-flow.gpg | gpg --import -i -

    aur_deps=(
        "eww-git"
        "papirus-folders"
        "poweralertd"
        "ttf-gabarito-git"
        "ttf-aporetic"
        "breezex-cursor-theme"
        "wayland-pipewire-idle-inhibit"
    )

    for d in "${aur_deps[@]}"; do
        install_aur_package "$d"
    done
}

function install_intel_legacy_drivers() {
    deps=(
        "mesa-amber"
        #"lib32-mesa-amber"
        "xf86-video-intel"
        "libva-intel-driver"
        "linux-firmware-intel"
        "intel-media-sdk"
        "libvdpau-va-gl"
    )
    for d in "${deps[@]}"; do
        install_package "$d"
    done
    echo "LIBVA_DRIVER_NAME=i965
VDPAU_DRIVER=va_gl" | sudo tee /etc/environment >/dev/null
}

function install_intel_drivers() {
    deps=(
        "mesa"
        #"lib32-mesa"
        "intel-media-driver"
        "linux-firmware-intel"
        "vpl-gpu-rt"
        "libvdpau-va-gl"
        "vulkan-intel"
    )
    for d in "${deps[@]}"; do
        install_package "$d"
    done
    echo "LIBVA_DRIVER_NAME=iHD
VDPAU_DRIVER=va_gl" | sudo tee /etc/environment >/dev/null
}

function install_amd_drivers() {
    deps=(
        "mesa"
        "xf86-video-amdgpu"
        "vulkan-radeon"
        "libvdpau-va-gl"
    )
    for d in "${deps[@]}"; do
        install_package "$d"
    done
    echo "LIBVA_DRIVER_NAME=radeonsi
VDPAU_DRIVER=va_gl" | sudo tee /etc/environment >/dev/null
}

function install_window_manager() {
    wm=""
    echo "0. None
1. Hyprland
2. Labwc"
    while true; do
        read -p "Select window manager (0-2): " wm
        [[ "$wm" =~ [0-2] ]] && break
    done
    case "$wm" in
        "1") yzshell window_manager set hyprland --dont-uninstall ;;
        "2") yzshell window_manager set labwc --dont-uninstall ;;
    esac
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
        "1") install_intel_drivers ;;
        "2") install_intel_legacy_drivers ;;
        "3") install_amd_drivers ;;
    esac
}

function help() {
    echo "usage: ./install.sh [args]
    args:
        --refresh | -r: Refresh configs, don't do full setup (mainly for development).
        --update | -u: Update yzshell from github.
        --install-optional-deps | -o: Install optional dependencies."
    exit 0
}

function copy_data_dir() {
    name="$1"
    cp -rf "./${name}" "${DATA_DIR}/${name}"
    exit_if_failed $? "failed copy './${name}' to '${DATA_DIR}/${name}'" 
} 

#set -e

# ensure script run as user
if [ "$EUID" -eq 0 ]; then
    echo "Please do not run as root"
    exit 1
fi

refresh=1
update=1
optional_deps=1
for a in "$@"; do
    case "$a" in
        "-h" | "--help") help ;;
        "--refresh" | "-r") refresh=0 ;;
        "--update" | "-u") update=0 ;;
        "--install-optional-deps" | "-o") optional_deps=0 ;;
        *) echo "Error: argument '${a}' not recognised"; exit 1 ;;
    esac
done

[ $update -eq 0 ] && git pull

# copy data
[ -d "$DATA_DIR" ] && rm -rf "$DATA_DIR"
mkdir -p "$DATA_DIR"
exit_if_failed $? "failed to make directory '${DATA_DIR}'"

copy_data_dir "templates" &
copy_data_dir "assets" &
copy_data_dir "static" &
copy_data_dir "colourschemes" &
copy_data_dir "src" &

# full setup
if [ $refresh -eq 1 ]; then
    sudo pacman -Syu
    install_yay
    install_deps
    [ $optional_deps -eq 0 ] && install_optional_deps
    install_graphics_drivers
    sudo systemctl enable fstrim.timer
    configure_zsh
    install_executable
    install_window_manager
    yzshell default_apps install_all
else
    [ $optional_deps -eq 0 ] && sudo pacman -Syu && install_optional_deps
fi

yzshell reconfigure

echo ">> Switch to Zsh with 'chsh -s \"\$(which zsh)\"'"
echo "Installation complete!"
