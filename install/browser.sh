function install_zen() {
    announce "Installing Zen Browser..."
    install_aur_pkgs "zen-browser-bin"
    zenconf -nu -nj
    yzconf set "web_browser" "zen-browser"
}

function other_browser() {
    cmd=""
    while true; do
        cmd="$(input 'Enter web browser command...')"
        confirm "Set '${cmd}' as web browser?" && break
    done
    yzconf set "web_browser" "${cmd}"
}

function install_browser() {
    which zen-browser >/dev/null 2>&1 && yzconf set "web_browser" "zen-browser" && return
    br="$(choose 'Select web browser...' 'Zen' 'I already have a web browser')"
    case "${br}" in
        "Zen") install_zen ;;
        "I already have a web browser") other_browser ;;
    esac
}
