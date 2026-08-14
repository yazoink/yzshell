function pkg_installed() {
    pacman -Qi "$1" >/dev/null 2>&1
    return $?
}

function aur_pkg_installed() {
    yay -Qi "$1" >/dev/null 2>&1
    return $?
}

function install_aur_pkg() {
    aur_pkg_installed "$1"
    if [ $? -ne 0 ]; then
        echo ">> Installing package ${1}..."
        yay -S --needed --norebuild --noredownload --noconfirm "$1"
        exit_if_failed $? "failed to install package '${1}'"
    fi
}

function install_pkg() {
    pkg_installed "$1"
    if [ $? -ne 0 ]; then
        echo ">> Installing package ${1}..."
        sudo pacman -S -y --needed --noconfirm "$1"
        exit_if_failed $? "failed to install package '${1}'"
    fi
}

function install_pkgs() {
    for p in "$@"; do
        install_pkg "$p"
    done
}

function install_aur_pkgs() {
    for p in "$@"; do
        install_aur_pkg "$p"
    done
}
