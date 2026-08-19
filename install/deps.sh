DEPS=(
    "base-devel"
    "stow"
    "freetype2"
    "vim"
    "nvim"
    "yazi"
    "qt5-wayland"
    "qt6-wayland"
    "qt5ct"
    "qt6ct"
    "kvantum"
    "kvantum-qt5"
    "direnv"
    "xorg-xwayland"
    "polkit"
    "jq"
    "curl"
    "wget"
    "lm_sensors"
    "mako"
    "libnotify"
    "waybar"
    "otf-font-awesome"
    "ttf-nerd-fonts-symbols"
    "tex-gyre-fonts"
    "hyprpicker"
    "wl-clipboard"
    "grim"
    "slurp"
    "swaybg"
    "python"
    "python-gobject"
    "python-pillow"
    #"python-beautifulsoup4"
    #"python-lxml"
    "python-requests"
    "gsettings-desktop-schemas"
    "dconf"
    "psmisc"
    "bc"
    "playerctl"
    "xdg-desktop-portal-gtk"
    "xdg-desktop-portal-wlr"
    "xdg-utils"
    "papirus-icon-theme"
    "swayosd"
    "hypridle"
    "brightnessctl"
    "hyprlock"
    #"network-manager-applet"
    #"nm-connection-editor"
    #"pavucontrol"
    "eza"
    "gnome-keyring"
    "adw-gtk-theme"
    "man-db"
    "wofi"
    "polkit"
    "hyprland"
    "xdg-desktop-portal-hyprland"
    "hyprland-qt-support"
    "mate-polkit"
    "pkgconf"
    "cpio"
    "cmake"
    "meson"
    "gcc"
    "pigz"
    "pbzip2"
    "bluez"
    "bluez-utils"
    "blueman"
)

AUR_DEPS=(
    "python-chevron"
    "eww-git"
    "papirus-folders"
    "poweralertd"
    "ttf-gabarito-git"
    "ttf-aporetic"
    "breezex-cursor-theme"
    "wayland-pipewire-idle-inhibit"
    #"hyprland-git"
    #"hyprland-plugin-hyprbars"
)

function deps_import_gpg_keys() {
    if ! aur_pkg_installed "eww-git"; then
        echo ">> Importing GPG keys for EWW"
        curl -sS https://github.com/elkowar.gpg | gpg --batch --import -
        curl -sS https://github.com/web-flow.gpg | gpg --batch --import -
    fi
}

function install_oh_my_zsh() {
    # oh-my-zsh
    if [ ! -d ~/.oh-my-zsh ]; then
        if ! answer_yes "Install and configure Zsh with yzshell?"; then
            yzconf set "configure_zsh" "false"
        fi
        yzconf set "configure_zsh" "true"
        pkgs=("zsh" "zsh-completions")
        install_pkgs "${pkgs[@]}"
        sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" "" --unattended
        exit_if_failed $? "failed to download oh-my-zsh"
        # autosuggestions
        [ ! -d "${HOME}/.oh-my-zsh/plugins/zsh-autosuggestions" ] &&
        git clone https://github.com/zsh-users/zsh-autosuggestions "${HOME}/.oh-my-zsh/plugins/zsh-autosuggestions"
        exit_if_failed $? "failed to download zsh-autosuggestions"
        # syntax highlighting
        [ ! -d "${HOME}/.oh-my-zsh/plugins/zsh-syntax-highlighting" ] &&
        git clone https://github.com/zsh-users/zsh-syntax-highlighting.git "${HOME}/.oh-my-zsh/plugins/zsh-syntax-highlighting"
        exit_if_failed $? "failed to download zsh-syntax-highlighting"
    fi
}

function install_mpd() {
    pkgs=(
        "mpd"
        "mpc"
        "ncmpcpp"
        "ario"
    )
    aur_pkgs=("mpdris2-rs")
    install_pkgs "${pkgs[@]}"
    install_aur_pkgs "${aur_pkgs[@]}"
    systemctl --user --now enable mpd
    systemctl --user --now enable mpdris2-rs.service
    echo ">> MPD installed"
}
