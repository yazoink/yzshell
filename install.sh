#!/usr/bin/env bash

DATA_DIR="${HOME}/.local/share/yzshell"

function configure_fonts() {
    [ ! -d "${HOME}/.fonts" ] && mkdir -p "${HOME}/.fonts"
    cp -rf "./static/.fonts/"* "${HOME}/.fonts"
    echo "Copied fonts"
    fc-cache -fv &> /dev/null
}

function configure_gtk() {
    [ ! -d "${HOME}/.themes" ] && mkdir -p "${HOME}/.themes"
    cp -rf "./static/.themes/"* "${HOME}/.themes"
    echo "Copied GTK themes"
}

function configure_icons() {
    [ ! -d "${HOME}/.icons" ] && mkdir -p "${HOME}/.icons"
    cp -rf "./static/.icons/"* "${HOME}/.icons"
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
}

function install_executable() {
    sudo install -Dm755 "./bin/yzshell" "/usr/bin/yzshell"
    echo "Installed 'yzshell' to '/usr/bin'"
}

function install_yay() {
    sudo pacman -S --needed base-devel git
    mkdir ~/src
    git clone https://aur.archlinux.org/yay.git ~/src/yay
    (
        cd ~/src/yay || exit 1
        makepkg -si
        
    )
}

function install_optional_deps() {
    deps=(
        "code"
        "fastfetch"
        "gimp"
    )
    for d in "${deps[@]}"; do
        sudo pacman -S "$d"
    done

    aur_deps=(
        "vesktop-bin"
    )

    for d in "${aur_deps[@]}"; do
        yay -S "$d"
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
        "mate-polkit"
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
        "swaylock"
        "network-manager-applet"
        "wayland-pipewire-idle-inhibit"
        "pavucontrol"
        "zsh"
        "zsh-completions"
        "eza"
        "gnome-keyring"
    )

    for d in "${deps[@]}"; do
        sudo pacman -S --needed "$d"
    done

    curl -sS https://github.com/elkowar.gpg | gpg --import -i -
    curl -sS https://github.com/web-flow.gpg | gpg --import -i -

    aur_deps=(
        "eww-git"
        "papirus-folders"
        "poweralertd"
        "ttf-gabarito-git"
        "ttf-aporetic"
    )

    for d in "${aur_deps[@]}"; do
        yay -S "$d"
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
        sudo pacman -S "$d"
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
        sudo pacman -S "$d"
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
        sudo pacman -S "$d"
    done
    echo "LIBVA_DRIVER_NAME=radeonsi
VDPAU_DRIVER=va_gl" | sudo tee /etc/environment >/dev/null
}

function install_labwc() {
    deps=(
        "labwc"
        "wlopm"
        "wtype"
    )
    for d in "${deps[@]}"; do
        sudo pacman -S "$d"
    done
    aur_deps=(
        "labwc-menu-generator-git"
    )
    for d in "${aur_deps[@]}"; do
        yay -S "$d"
    done
    echo "{ \"window_manager\": \"labwc\" }" > "${HOME}/.config/yzshell/config.json"
}

function install_hyprland() {
    deps=(
        "hyprland"
        "xdg-desktop-portal-hyprland"
        "pkgconf"
        "cpio"
        "cmake"
        "git"
        "meson"
        "gcc"
    )
    for d in "${deps[@]}"; do
        sudo pacman -S --needed "$d"
    done
    echo "{ \"window_manager\": \"hyprland\" }" > "${HOME}/.config/yzshell/config.json"
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
        "1") install_hyprland & ;;
        "2") install_labwc & ;;
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

cp -rf "./templates" "${DATA_DIR}/templates" &
cp -rf "./colourschemes" "${DATA_DIR}/colourschemes" &
cp -rf "./assets" "${DATA_DIR}/assets" &
cp -rf "./static" "${DATA_DIR}/static" &
cp -rf "./src" "${DATA_DIR}/src" &

# full setup
if [ $refresh -eq 1 ]; then
    sudo pacman -Syu
    install_yay
    install_deps
    [ $optional_deps -eq 0 ] && install_optional_deps
    install_graphics_drivers
    install_window_manager
    sudo systemctl enable fstrim.timer
    configure_zsh
    configure_fonts
    configure_gtk
    configure_icons
    install_executable
    yzshell default_apps install_all
else
    [ $optional_deps -eq 0 ] && install_optional_deps
fi

yzshell reconfigure &>/dev/null

echo ">> Switch to Zsh with 'chsh -s \"\$(which zsh)\"'"
echo ">> After launching Hyprland, enable Hyprbars plugin:
$ hyprpm update
$ hyprpm add https://github.com/hyprwm/hyprland-plugins
$ hyprpm enable hyprbars"
echo "Installation complete!"
