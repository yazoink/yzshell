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
        source "${REPO_DIR}/install/install-yay.sh"
        announce "Installed yay!"
    fi
    bash -c "${REPO_DIR}/install/copy-files.py"
    announce "Files copied!"
    bash -c "${REPO_DIR}/install/configure-env.py"
    source "${ENV_FILE}"
    announce "Environment variables configured!"
    if $install_deps; then
        announce "Installing dependencies..."
        bash -c "${REPO_DIR}/install/install-deps.py ${REPO_DIR}/misc/deps.json"
        announce "Installed dependencies!"
        announce "Installing Vscodium extensions..."
        bash -c "${REPO_DIR}/install/install-vscode-extensions.py"
        announce "Installed Vscodium extensions!"
        source "${REPO_DIR}/install/configure-greetd.sh" >/dev/null 2>&1
        bash -c "${REPO_DIR}/install/configure-default-apps.py"
        bash -c "${REPO_DIR}/install/configure-gpu-drivers.py"
        sudo ln -sf /usr/share/fontconfig/conf.avail/10-nerd-font-symbols.conf \
            /etc/fonts/conf.d/
        sudo journalctl --vacuum-time=2weeks
        sudo systemctl enable --now fstrim.timer
        sudo systemctl enable --now systemd-oomd
        sudo systemctl enable --now swayosd-libinput-backend.service
        sudo systemctl enable --now bluetooth.service
        systemctl --user --now enable mpd
    fi
    if $install_opt_deps; then
        announce "Installing optional dependencies..."
        bash -c "${REPO_DIR}/install/install-deps.py ${REPO_DIR}/misc/optional-deps.json"
        announce "Installed optional dependencies!"
    fi

    omz_dir=~/.oh-my-zsh
    if [ ! -n "${omz_dir}" ]; then
        install_pkgs zsh zsh-completions
        sh -c \
            "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" \
            "" --unattended
        sudo chsh -s "$(which zsh)"
        announce "Zsh installed"
    fi

    if ! yzconf deploy_configs -r; then
        exit 1
    fi
    pgrep --quiet Hyprland && yzshell reload >/dev/null 2>&1

    reset

    gum style \
        --foreground="${COL2}" \
        --padding='2 4' \
        "$(figlet "yzshell")"

    echo "A reboot is required after the initial installation!

To configure Zen browser: once there is at least one profile in '~/.config/zen', run 'zenconf --select-profile' to ensure its configuration.

Make sure Pipewire is installed, and NetworkManager is in use!"
}

function announce() {
    gum style --foreground "${COL1}" "$@"
}

function confirm() {
    #read -p "${@} [Y/n]: " a
    #if [[ "${a^^}" = "YES" ]] || [[ "${a^^}" = "Y" ]] || [[ "${a}" = "" ]]; then
    #    return 0
    #else
    #    return 1
    #fi
    gum confirm --padding="1 1" "$1"
}

function install_pkgs() {
    sudo pacman -S --needed --noconfirm "$@"
}

main "$@"