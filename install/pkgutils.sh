function pkg_installed() {
    pacman -Qi "$1" >/dev/null 2>&1
    return $?
}

function aur_pkg_installed() {
    yay -Qi "$1" >/dev/null 2>&1
    return $?
}

function install_aur_pkgs() {
    for pkg in "${@}"; do
        aur_pkg_installed "${pkg}" && continue
        yay -S --needed --norebuild --noredownload --noconfirm "${pkg}"
        exit_if_failed $? "Failed to install '${pkg}'"
    done
}

function install_pkgs() {
    for pkg in "${@}"; do
        pkg_installed "${pkg}" && continue
        sudo pacman -S -y --needed --noconfirm "${pkg}"
        exit_if_failed $? "Failed to install '${pkg}'"
    done
}
