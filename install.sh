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
    "yzctl"
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
    "scripts"
    "lib"
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
    echo ""
    announce "Chaotic AUR enabled!"
}

function configure_env_vars() {
    env_file="/etc/environment"
    data_dir="${HOME}/.local/share/yzshell"
    script_dir="${data_dir}/scripts"
    conf_dir="${HOME}/.config/yzshell"
    cache_dir="${HOME}/.cache/yzshell"
    lib_dir="${data_dir}/lib"
    declare -A env_vars=(
        ["YZSHELL_DATA_DIR"]="${data_dir}"
        ["YZSHELL_LIB_DIR"]="${lib_dir}"
        ["YZSHELL_PYTHON_LIB_DIR"]="${lib_dir}/python"
        ["YZSHELL_BASH_LIB_DIR"]="${lib_dir}/bash"
        ["YZSHELL_STOW_DIR"]="${HOME}/.dotfiles"
        ["YZSHELL_CONF_DIR"]="${conf_dir}"
        ["YZSHELL_CONF_FILE"]="${conf_dir}/config.json"
        ["YZSHELL_DEFAULT_CONF_FILE"]="${data_dir}/misc/default-config.json"
        ["YZSHELL_EWW_DIR"]="${HOME}/.config/eww"
        ["YZSHELL_SCRIPT_DIR"]="${script_dir}"
        ["YZSHELL_EWW_SCRIPT_DIR"]="${script_dir}/eww"
        ["YZSHELL_COLOURS_DIR"]="${data_dir}/colourschemes"
        ["YZSHELL_TEMPLATES_DIR"]="${data_dir}/templates"
        ["YZSHELL_CACHE_DIR"]="${cache_dir}"
        ["YZSHELL_TEMPLATE_CACHE_DIR"]="${cache_dir}/built_templates"
        ["YZSHELL_WALLPAPER_CACHE_DIR"]="${cache_dir}/wallpapers"
        ["YZSHELL_WALLPAPER_LOCKFILE"]="${cache_dir}/wallpapers.lock"
    )
    for v in "${!env_vars[@]}"; do
        export "${v}=${env_vars[$v]}"
        if grep "${v}" "${env_file}"; then
            sudo gawk -i inplace "!/${v}/" "${env_file}"
        fi
        echo "${v}=${env_vars[$v]}" \
            | sudo tee -a "${env_file}" >/dev/null 2>&1
    done
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

function backup_file() {
    if [ -L "${1}" ]; then # remove if symlink
        rm "${1}"
        announce "Removed conflicting symlink: ${1}"
    elif [ -f "${1}" ]; then # if file
        mv "${1}" "${1}.bak"
        announce "Backed up conflicting file '${1}' to '${1}.bak'"
    elif [ -d "${1}" ]; then # if dir
        mv "${1}" "${1}-old"
        announce "Backed up conflicting directory '${1}' to '${1}-old'"
    fi
}

# takes name of dir in dotfiles/ as arg
function backup_dots_dir() {
    d="$(basename "${1}")"
    for file in "${1}"/*; do
        f="$(basename "${file}")"
        backup_file "${HOME}/${d}/${f}"
    done
}

function announce() {
    gum style --foreground 212 "${@}"
}

function confirm() {
    gum confirm \
        --padding="1 0" \
        "${1}"
}

function choose() {
    gum choose \
        --padding="1 0" \
        --header "${1}" \
        "${@:2}"
}

function input() {
    gum input \
        --padding="1 0" \
        --placeholder "${1}"
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
    if [ "$EUID" -eq 0 ]; then
        gum log --structured --level="fatal" "Please do not run as root"
        exit 1
    fi

    # PARSE ARGS
    install_deps=0
    install_local=1
    install_opt_deps=1
    dir_index=-1
    i=1
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
            if confirm "Directory '${SRC_DIR}' already exists, overwrite?"; then
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

    # ENV VARS
    configure_env_vars >/dev/null 2>&1

    # INSTALL ESSENTIAL DEPS
    source "${SRC_DIR}/install/pkgutils.sh"
    ! pkg_installed "git" &&
    install_pkgs "git"
    if ! pkg_installed "yay"; then
        install_yay
    fi
    if ! grep -q "chaotic-aur" /etc/pacman.conf; then
        confirm "Enable Chaotic AUR?" &&
        enable_chaotic_aur
    fi

    # COPY FILES
    source "${SRC_DIR}/install/copyutils.sh"
    copy_files

    # INSTALL DEPS
    if [ $install_deps -eq 0 ]; then
        source "${SRC_DIR}/install/deps.sh"
        source "${SRC_DIR}/install/filemanager.sh"
        source "${SRC_DIR}/install/terminal.sh"
        source "${SRC_DIR}/install/browser.sh"
        source "${SRC_DIR}/install/gpu.sh"
        deps_import_gpg_keys
        install_pkgs "${DEPS[@]}"
        install_aur_pkgs "${AUR_DEPS[@]}"
        sudo sh -c 'ln -s /usr/share/fontconfig/conf.avail/10-nerd-font-symbols.conf \
            /etc/fonts/conf.d/ >/dev/null 2>&1 &'
        sudo sh -c 'journalctl --vacuum-time=2weeks >/dev/null 2>&1'
        sudo sh -c 'systemctl enable --now fstrim.timer >/dev/null 2>&1'
        sudo sh -c 'systemctl enable --now systemd-oomd >/dev/null 2>&1'
        sudo sh -c 'systemctl enable --now swayosd-libinput-backend.service >/dev/null 2>&1'
        sudo sh -c 'systemctl enable --now bluetooth.service >/dev/null 2>&1'
        if confirm "Configure Zsh with yzshell?"; then
            install_oh_my_zsh
            yzconf set "configure_zsh" "true"
        else
            yzconf set "configure_zsh" "false"
        fi
        if confirm "Configure Neovim with yzshell?"; then
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

    # INSTALL OPTIONAL DEPS
    if [ $install_opt_deps -eq 0 ]; then
        source "${SRC_DIR}/install/optdeps.sh"
        install_pkgs "${OPT_DEPS[@]}"
        install_aur_pkgs "${OPT_AUR_DEPS[@]}"
        install_dict
        install_soundboard
        if confirm "Install and configure Vscodium with yzshell?"; then
            yzconf set "configure_vscodium" "true"
            install_vscode
        else
            yzconf set "configure_vscodium" "false"
        fi
        if confirm "Install and configure Vesktop with yzshell?"; then
            yzconf set "configure_vesktop" "true"
            install_aur_pkgs "vesktop-bin"
        else
            yzconf set "configure_vesktop" "false"
            # announce "A Vesktop theme, which can be enabled manually, will still be created"
        fi
    fi

    # BACK UP CONFLICTING DOTFILES
    shopt -s dotglob
    for file in "${SRC_DIR}/dotfiles"/*; do
        f="$(basename "${file}")"
        t="${HOME}/${f}"
        if [ -d "${t}" ]; then
            backup_dots_dir "${SRC_DIR}/dotfiles/${f}"
        elif [ -f "${t}" ]; then
            backup_file "${t}"
        fi
    done
    for f in $(cat "${SRC_DIR}/templates/templates.json" | jq -r -c '.[]'); do
        backup_file "${HOME}/${f}"
        break
    done
    shopt -u dotglob
    (
        yzconf deploy_configs -r
        hyprland_running && yzshell reload
    ) >/dev/null 2>&1 & disown

    # REMOVE SOURCE IF GIT INSTALL
    if [ $install_local -ne 0 ]; then
        if confirm "Delete repo at '${SRC_DIR}'?"; then
            rm -rf "${SRC_DIR}"
            announce "Repo deleted"
        fi
    fi

    # SWITCH TO ZSH?
    zsh="$(which zsh)"
    if [ "${SHELL}" != "${zsh}" ] && [ "$(yzconf get configure_zsh)" == "true" ]; then
        confirm "Set Zsh as default shell?" && chsh -s "${zsh}"
    fi

    # END NOTES
    notes="A reboot is required after the initial installation.

To configure Zen Browser: once there is at least one profile in '~/.config/zen', run 'zenconf --select-profile' to ensure its configuration.

Make sure Pipewire is installed and NetworkManager is in use!

Hyprland is configured to start on TTY login from '~/.zprofile'; if you are not using Zsh, it will need to be launched manually with 'exec dbus-run-session start-hyprland', or from a display manager."
    gum style \
        --border-foreground 212 \
        --foreground 212 \
        --padding "2 4" \
        "$(figlet "yzshell")"
    gum format '{{ Bold "Notes:" }}' -t template
    echo "

$notes"
}

main "$@"