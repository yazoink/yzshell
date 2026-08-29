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
    "base16-to-yzshell-scheme"
    "base16-to-yzshell-template"
)
DIRECTORIES=(
    "assets"
    "colourschemes"
    "dotfiles"
    "templates"
    "misc"
)

function exit_if_failed() {
    ret=$1
    error_msg="$2"
    if [ $ret -ne 0 ]; then
        gum log --structured --level="fatal" "${error_msg}"
        exit 1
    fi
}

function enable_chaotic_aur() {
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
    sudo pacman -Syu --noconfirm
}

function install_yay() {
    local -
    set -e
    ! pkg_installed "base-devel" && install_pkgs "base-devel"
    mkdir ~/src
    git clone https://aur.archlinux.org/yay.git ~/src/yay
    exit_if_failed $? "failed to download yay"
    (
        cd ~/src/yay
        makepkg -si
    )
}

function copy_files() {
    local -
    set -e
    [ -d $TARGET_DIR ] && rm -rf $TARGET_DIR
    mkdir -p $TARGET_DIR
    for d in "${DIRECTORIES[@]}"; do
        copy_data_dir "${d}"
    done
    for e in "${EXECUTABLES[@]}"; do
        copy_executable "${e}"
    done
}

function announce() {
    gum style --foreground 212 "${@}"
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
        gum log --structured --level="fatal" "Please do not run as root"
        exit 1
    fi
    # gum style \
        #     --foreground 212 \
        #     --border double \
        #     --border-foreground 212 \
        #     --padding "1 2" \
        #     --margin 1 \
        #     "Installing yzshell!"
    for a in "$@"; do
        case "$a" in
            "-n" | "--no-deps") install_deps=1 ;;
            "-l" | "--local") install_local=0 ;;
            "-d" | "--dir") dir_index=$((i + 1)) ;;
            "-o" | "--optional-deps") install_opt_deps=0 ;;
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
        announce "Installing from local repo: '${SRC_DIR}'"
    else # git install
        announce "Installing from Github"
        [ $dir_index -ne -1 ] && SRC_DIR="${!dir_index}"
    fi
    # IF GIT INSTALL, CLONE REPO
    if [ $install_local -ne 0 ]; then
        clone=0
        if [ -d "$SRC_DIR" ]; then
            clear
            if gum confirm "Directory '${SRC_DIR}' already exists, overwrite?"; then
                rm -rf "${SRC_DIR}"
            else
                clone=1
            fi
        fi
        if [ $clone -eq 0 ]; then
            gum spin \
                --spinner dot \
                --title "Cloning yzshell to '${SRC_DIR}'..." -- \
                git clone "https://github.com/yazoink/yzshell.git" "$SRC_DIR"
            exit_if_failed $? "Could not clone repo."
        fi
    fi
    # INSTALL ESSENTIAL DEPS
    source "${SRC_DIR}/install/pkgutils.sh"
    ! pkg_installed "git" &&
    install_pkgs "git"
    if ! pkg_installed "yay"; then
        export -f install_yay
        gum spin --spinner dot --title "Installing yay..." -- \
            bash -c install_yay
    fi
    if ! grep -q "chaotic-aur" /etc/pacman.conf; then
        export -f enable_chaotic_aur
        gum confirm "Enable Chaotic AUR?" &&
        gum spin --spinner dot --title "Enabling Chaotic AUR..." -- \
            bash -c enable_chaotic_aur
    fi
    source "${SRC_DIR}/install/copyutils.sh"
    copy_files
    # INSTALL DEPS
    if [ $install_deps -eq 0 ]; then
        source "${SRC_DIR}/install/deps.sh"
        deps_import_gpg_keys
        install_pkgs "${DEPS[@]}"
        install_aur_pkgs "${AUR_DEPS[@]}"
        sudo ln -s /usr/share/fontconfig/conf.avail/10-nerd-font-symbols.conf \
            /etc/fonts/conf.d/ >/dev/null 2>&1 &
        sudo journalctl --vacuum-time=2weeks >/dev/null 2>&1
        sudo systemctl enable --now fstrim.timer >/dev/null 2>&1
        sudo systemctl enable --now systemd-oomd >/dev/null 2>&1
        sudo systemctl enable --now swayosd-libinput-backend.service >/dev/null 2>&1
        sudo systemctl enable --now bluetooth.service >/dev/null 2>&1
    fi
    # INSTALL OPTIONAL DEPS
    if [ $install_opt_deps -eq 0 ]; then
        source "${SRC_DIR}/install/optdeps.sh"
        install_pkgs "${OPT_DEPS[@]}"
        install_aur_pkgs "${OPT_AUR_DEPS[@]}"
        install_dict
        install_soundboard
        clear
        if gum confirm "Install and configure Vscodium with yzshell?"; then
            yzconf set "configure_vscodium" "true"
            install_vscode
        else
            yzconf set "configure_vscodium" "false"
        fi
        clear
        if gum confirm "Install and configure Vesktop with yzshell?"; then
            yzconf set "configure_vesktop" "true"
            install_aur_pkgs "vesktop-bin"
        else
            yzconf set "configure_vesktop" "false"
            announce "A Vesktop theme, which can be enabled manually, will still be created"
        fi
    fi
    if [ $install_deps -eq 0 ]; then
        source "${SRC_DIR}/install/filemanager.sh"
        source "${SRC_DIR}/install/terminal.sh"
        source "${SRC_DIR}/install/browser.sh"
        source "${SRC_DIR}/install/gpu.sh"
        install_oh_my_zsh
        clear
        if gum confirm "Configure Neovim with yzshell?"; then
            yzconf set "configure_nvim" "true"
        else
            yzconf set "configure_nvim" "false"
        fi
        install_file_manager
        install_terminal
        install_browser
        install_gpu_drivers
        install_mpd
    fi
    yzconf deploy_configs -r
    # REMOVE SOURCE IF GIT INSTALL
    if [ $install_local -ne 0 ]; then
        if gum confirm "Delete repo at '${SRC_DIR}'?"; then
            rm -rf "${SRC_DIR}"
            echo ">> Repo deleted"
        fi
    fi
    gum style "" # the output gets garbled if i don't put this here, idk why
    notes="A reboot is recommended after the initial installation.

To configure Zen Browser: once there is at least one profile in '~/.config/zen', run 'zenconf --select-profile' to ensure its configuration.

Make sure Pipewire is installed and NetworkManager is in use!

Run 'sudo chsh -s \"\$(which zsh)\"' to switch to Zsh.

Hyprland is configured to start on TTY login from '~/.zprofile'; if you are not using Zsh, it will need to be launched manually with 'exec dbus-run-session start-hyprland', or from a display manager."
    reset
    gum style \
        --foreground 212 \
        --border-foreground 212 \
        --margin "1 2" \
        --padding "2 4" \
        --border double \
        "Thank you for installing yzshell!"
    gum format '{{ Bold "Notes:" }}' -t template
    echo "

$notes"
}

main "$@"
