function install_zen() {
    announce "Installing Zen Browser..."
    install_aur_pkgs "zen-browser-bin"
    yzconf set "web_browser" "zen-browser"
}

function other_browser() {
    clear
    cmd=""
    while true; do
        clear
        cmd="$(gum input --placeholder 'Enter web browser command...')"
        gum confirm "Set '${cmd}' as web browser?" && break
    done
    yzconf set "web_browser" "${cmd}"
}

function install_browser() {
    which zen-browser >/dev/null 2>&1 && yzconf set "web_browser" "zen-browser" && return
    clear
    br="$(gum choose --header 'Select web browser...' 'Zen' 'I already have a web browser')"
    case "${br}" in
        "Zen") install_zen ;;
        "I already have a web browser") other_browser ;;
    esac
}
