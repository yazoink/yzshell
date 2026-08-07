#!/usr/bin/env bash

# TODO: configure zen, optionally install nvim and deps, do something about 
# hyprbars

TARGET_DIR=~/.local/share/yzshell
SRC_DIR=/tmp/yzshell

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
        local -; set -e
        echo ">> Enabling Chaotic AUR"
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
}

function install_yay() {
    pkg_installed "yay"
    if [ $? -ne 0 ]; then
        echo ">> Installing yay..."
        local -; set -e
        sudo pacman -S -y --needed base-devel
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
    local -; set -e
    source "${SRC_DIR}/install/copyutils.sh"
    [ -d $TARGET_DIR ] && rm -rf $TARGET_DIR
    mkdir -p $TARGET_DIR
    copy_data_dir "assets"
    copy_data_dir "colourschemes"
    copy_data_dir "dotfiles"
    copy_data_dir "templates"
    copy_executable "yzconf"
    copy_executable "yzshell"
    copy_executable "yzwallpaper"
    copy_executable "yzwidgets"
    copy_executable "yzpicker"
    copy_executable "yzrecorder"
    copy_executable "yzshot"
    copy_executable "iconfetch"
}

function main() {
    install_deps=1
    install_local=0
    install_opt_deps=0
    dir_index=-1
    i=1
    for a in "$@"; do
        case "$a" in
            "-n" | "--no-deps") install_deps=0 ;;
            "-l" | "--local") install_local=1 ;;
            "-d" | "--dir") dir_index=$((i+1)) ;;
            "-o" | "--optional-deps") install_opt_deps=1 ;;
        esac
        i+=1
    done
    # GET SRC DIR
    if [ $install_local -eq 1 ]; then   # local install
        if [ $dir_index -gt 0 ]; then   # dir specified
            SRC_DIR="${!dir_index}"
        else                            # dir not specified
            SRC_DIR="$( 
                cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" \
                &> /dev/null && pwd
            )"
        fi
    else                                # git install
        [ $dir_index -gt 0 ] && SRC_DIR="${!dir_index}"
    fi
    # INSTALL ESSENTIAL DEPS
    source "${SRC_DIR}/install/pkgutils.sh"
    install_pkg "git"
    install_yay
    enable_chaotic_aur
    # IF GIT INSTALL, CLONE REPO
    if [ $install_local -eq 0 ]; then
        echo ">> Cloning yzshell..."
        git clone "https://github.com/yazoink/yzshell.git" "$SRC_DIR"
        exit_if_failed $? "could not clone repo."
    fi
    # INSTALL DEPS
    if [ $install_deps -eq 1 ]; then
        source "${SRC_DIR}/install/deps.sh"
        deps_import_gpg_keys
        install_pkgs "${DEPS[@]}"
        install_aur_pkgs "${AUR_DEPS[@]}"
    fi
    # INSTALL OPTIONAL DEPS
    if [ $install_opt_deps -eq 1 ]; then
        source "${SRC_DIR}/install/optdeps.sh"
        install_pkgs "${OPT_DEPS[@]}"
        install_aur_pkgs "${OPT_AUR_DEPS[@]}"
        install_dict
        install_soundboard
    fi
    # COPY FILES
    copy_files
    yzconf deploy_configs -r
    # SET GTK THEME/FONT
    gsettings set org.gnome.desktop.interface gtk-theme adw-gtk3
    gsettings set org.gnome.desktop.interface font-name "sans 11"
    # REMOVE SOURCE IF GIT INSTALL
    if [ $install_local -eq 0 ]; then
        rm -rf "$SRC_DIR"
    fi
}

main "$@"