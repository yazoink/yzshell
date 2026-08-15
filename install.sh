#!/usr/bin/env bash

TARGET_DIR=~/.local/share/yzshell
SRC_DIR=/tmp/yzshell
EXECUTABLES=(
    "yzconf"
    "yzshell"
    "yzwallpaper"
    "yzwidgets"
    "yzpicker"
    "yzrecorder"
    "yzshot"
    "iconfetch"
    "zenconf"
    "yzshell-install-hyprland-plugins"
)
DIRECTORIES=(
    "assets"
    "colourschemes"
    "dotfiles"
    "templates"
    "misc"
)

function answer_yes() {
    while true; do
        read -p ">> $1 [Y/n]: " answer
        case "${answer^^}" in
            "" | "Y" | "YES") return 0 ;;
            "N" | "NO") return 1 ;;
        esac
    done
}

function exit_if_failed() {
    ret=$1
    error_msg="$2"
    if [ $ret -ne 0 ]; then
        echo "Error: ${error_msg}"
        exit 1
    fi
}

function enable_chaotic_aur() {
    if ! grep -q "chaotic-aur" /etc/pacman.conf; then
        if answer_yes "Enable Chaotic AUR repo?"; then
            local -
            set -e
            sudo pacman-key --init
            sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
            sudo pacman-key --lsign-key 3056513887B78AEB
            sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst'
            sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'
            echo "
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist
            " | sudo tee -a /etc/pacman.conf
            sudo pacman -Syu
        fi
    fi
}

function install_yay() {
    pkg_installed "yay"
    if [ $? -ne 0 ]; then
        echo ">> Installing yay..."
        local -
        set -e
        sudo pacman -S --needed --no-confirm base-devel
        mkdir ~/src
        git clone https://aur.archlinux.org/yay.git ~/src/yay
        exit_if_failed $? "failed to download yay"
        (
            cd ~/src/yay
            makepkg -si
        )
    fi
}

function copy_files() {
    local -
    set -e
    source "${SRC_DIR}/install/copyutils.sh"
    [ -d $TARGET_DIR ] && rm -rf $TARGET_DIR
    mkdir -p $TARGET_DIR
    for d in "${DIRECTORIES[@]}"; do
        copy_data_dir "${d}"
    done
    for e in "${EXECUTABLES[@]}"; do
        copy_executable "${e}"
    done
}

function help() {
    echo "Usage: ./install.sh [FLAGS]
    Flags:
        --optional-deps | -o: Install optional dependencies.
        --no-deps | -n: Skip installing dependencies (does not impact -o).
        --local | -l:
            Install from local directory instead of Github repo. Defaults to
            the script directory, but directory can be specified with -d.
        --dir | -d:
            Specify the directory to install from. When installing from Github,
            this is where the repo will be cloned to.
    "
    exit 0
}

function main() {
    install_deps=0
    install_local=1
    install_opt_deps=1
    dir_index=-1
    i=1
    if [ "$EUID" -eq 0 ]; then
        echo "Error: please do not run as root"
        exit 1
    fi
    for a in "$@"; do
        case "$a" in
            "-n" | "--no-deps") install_deps=1 ;;
            "-l" | "--local") install_local=0 ;;
            "-d" | "--dir") dir_index=$((i + 1)) ;;
            "-o" | "--optional-deps") install_opt_deps=0 ;;
            *) help ;;
        esac
        ((i = i + 1))
    done
    # GET SRC DIR
    if [ $install_local -eq 0 ]; then  # local install
        if [ $dir_index -ne -1 ]; then # dir specified
            SRC_DIR="${!dir_index}"
        else # dir not specified
            SRC_DIR="$(
                cd -- "$(dirname -- "${BASH_SOURCE[0]}")" \
                    &>/dev/null && pwd
            )"
        fi
        if [ ! -d "${SRC_DIR}/install" ]; then
            echo "Error: install utils not found."
            exit 1
        fi
        # ENSURE DATA FILES IN INSTALL DIR
        for d in "${DIRECTORIES[@]}"; do
            if [ ! -d "${SRC_DIR}/${d}" ]; then
                echo "Error: '${d}' not in '${SRC_DIR}'"
                exit 1
            fi
        done
        for e in "${EXECUTABLES[@]}"; do
            if [ ! -f "${SRC_DIR}/bin/${e}" ]; then
                echo "Error: '${e}' not in '${SRC_DIR}/bin'"
                exit 1
            fi
        done
        echo ">> Installing from local repo '${SRC_DIR}'"
    else # git install
        [ $dir_index -ne -1 ] && SRC_DIR="${!dir_index}"
    fi
    # INSTALL ESSENTIAL DEPS
    source "${SRC_DIR}/install/pkgutils.sh"
    install_pkg "git"
    install_yay
    enable_chaotic_aur
    # IF GIT INSTALL, CLONE REPO
    if [ $install_local -ne 0 ]; then
        echo ">> Cloning yzshell to '${SRC_DIR}'"
        clone=0
        if [ -d "$SRC_DIR" ]; then
            if answer_yes "Directory '${SRC_DIR}' already exists, overwrite?"; then
                rm -rf "${SRC_DIR}"
                pass
            else
                clone=1
            fi
        fi
        if [ $clone -eq 0 ]; then
            git clone "https://github.com/yazoink/yzshell.git" "$SRC_DIR"
            exit_if_failed $? "could not clone repo."
        fi
    fi
    # INSTALL DEPS
    if [ $install_deps -eq 0 ]; then
        source "${SRC_DIR}/install/deps.sh"
        deps_import_gpg_keys
        install_pkgs "${DEPS[@]}"
        install_aur_pkgs "${AUR_DEPS[@]}"
        install_oh_my_zsh
        if answer_yes "Configure nvim with yzshell?"; then
            yzconf set "configure_nvim" "true"
        else
            yzconf set "configure_nvim" "false"
        fi
    fi
    # INSTALL OPTIONAL DEPS
    if [ $install_opt_deps -eq 0 ]; then
        source "${SRC_DIR}/install/optdeps.sh"
        install_pkgs "${OPT_DEPS[@]}"
        install_aur_pkgs "${OPT_AUR_DEPS[@]}"
        install_dict
        install_soundboard
        if answer_yes "Install and configure Vscodium with yzshell?"; then
            yzconf set "configure_vscodium" "true"
            install_vscode
        else
            yzconf set "configure_vscodium" "false"
        fi
    fi
    copy_files
    if [ $install_deps -eq 0 ]; then
        source "${SRC_DIR}/install/filemanager.sh"
        source "${SRC_DIR}/install/terminal.sh"
        source "${SRC_DIR}/install/gpu.sh"
        install_file_manager
        install_terminal
        install_gpu_drivers
        install_mpd
    fi
    yzconf deploy_configs -r
    gsettings set org.gnome.desktop.interface gtk-theme adw-gtk3
    gsettings set org.gnome.desktop.interface font-name "sans 11"
    # REMOVE SOURCE IF GIT INSTALL
    if [ $install_local -ne 0 ]; then
        echo "REMOVE"
        if answer_yes "Delete repo at '${SRC_DIR}'?"; then
            rm -rf "${SRC_DIR}"
            echo ">> Repo deleted"
        fi
    fi
    echo "
#### NOTES ####
>> To configure Zen Browser: once there is at least one profile in
   ~/.config/zen, run 'zenconf --select-profile' to ensure its configuration."
    echo ">> Make sure Pipewire is installed and NetworkManager is in use! "
    echo ">> Run 'chsh -s \"\$(which zsh)\"' to switch to Zsh."
    echo ">> A reboot is recommended after the initial installation."
    echo "
Done!"
}

main "$@"
