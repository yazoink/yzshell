function pkg_installed() {
    pacman -Qi "$1" >/dev/null 2>&1
    return $?
}

function aur_pkg_installed() {
    yay -Qi "$1" >/dev/null 2>&1
    return $?
}

function install_aur_pkgs() {
    echo ">> Installing packages ${@}..."
    yay -S --needed --norebuild --noredownload --noconfirm "${@}"
    exit_if_failed $? "failed to install package '${@}'"
}

function install_pkgs() {
    echo ">> Installing packages ${@}..."
    sudo pacman -S -y --needed --noconfirm "${@}"
    exit_if_failed $? "failed to install package '${@}'"
}
