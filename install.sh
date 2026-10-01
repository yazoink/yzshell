#!/usr/bin/env bash

REPO_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
TARGET_DIR=~/.local/share/yzshell
ENV_FILE=$TARGET_DIR/env
COL1=212
COL2=99

function main() {
    install_deps=true
    install_opt_deps=false
    for arg in "$@"; do
        case "${arg}" in
            "-sd" | "--skip-deps") 
                install_deps=false 
                ;;
            "-o" | "--optional-deps") 
                install_opt_deps=true 
                ;;
        esac
    done

    export REPO_DIR
    export TARGET_DIR
    export ENV_FILE

    install_pkgs gum figlet coreutils which python
    if ! grep -q "chaotic-aur" "/etc/pacman.conf"; then
        if confirm "Enable chaotic-aur repo? (recommended)"; then
            sudo bash -c "${REPO_DIR}/install/enable-chaotic-aur.sh"
            announce "Enabled chaotic-aur repo!"
        fi
    fi
    if ! pacman -Qi yay >/dev/null 2>&1; then
        announce "Installing yay..."
        install_pkgs base-devel go
        bash -c "${REPO_DIR}/install/install-yay.sh"
        announce "Installed yay!"
    fi
    if $install_deps; then
        announce "Installing dependencies..."
        bash -c "${REPO_DIR}/install/install-deps.py ${REPO_DIR}/misc/deps.json"
        announce "Installed dependencies!"
    fi
    if $install_opt_deps; then
        announce "Installing optional dependencies..."
        bash -c "${REPO_DIR}/install/install-deps.py ${REPO_DIR}/misc/optional-deps.json"
        announce "Installed optional dependencies!"
    fi
    bash -c "${REPO_DIR}/install/copy-files.py"
    announce "Files copied!"
    bash -c "${REPO_DIR}/install/configure-env.py"
    announce "Environment variables configured!"

    yzconf deploy_configs -r
    pgrep --quiet Hyprland && yzshell reload >/dev/null 2>&1
}

function announce() {
    gum style --foreground "${COL1}" "$@"
}

function confirm() {
    gum confirm --padding="1 1" "$1"
}

function install_pkgs() {
    sudo pacman -S --needed --noconfirm "$@"
}

main "$@"