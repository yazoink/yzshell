function install_zen() {
    install_aur_pkgs "zen-browser-bin"
    yzconf set "web_browser" "zen-browser"
}

function other_browser() {
    cmd=""
    while true; do
        read -p ">> Enter web browser command: " cmd
        answer_yes "Set '${cmd}' as web browser?" && break
    done
    yzconf set "web_browser" "${cmd}"
}

function install_browser() {
    which zen-browser >/dev/null 2>&1 && yzconf set "web_browser" "zen-browser" && return
    br=""
    echo "
#### WEB BROWSER ####
1. Zen
3. I already have a web browser"
    while true; do
        read -p ">> Install web browser [1-2]: " br
        [[ "${br}" =~ [1-2] ]] && break
    done
    case "${br}" in
        "1") install_zen ;;
        "2") other_browser ;;
    esac
}
