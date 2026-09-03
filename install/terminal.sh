function install_alacritty() {
    install_pkgs "alacritty"
    yzconf set terminal alacritty
}

function install_foot() {
    install_pkgs foot
    yzconf set terminal foot
}

function install_ghostty() {
    install_pkgs ghostty
    yzconf set terminal ghostty
}

function install_kitty() {
    install_pkgs kitty
    yzconf set terminal kitty
}

function other_terminal() {
    cmd=""
    while true; do
        cmd="$(input 'Enter terminal command...')"
        confirm "Set '${cmd}' as terminal?" && break
    done
    yzconf set terminal "${cmd}"
}

function install_terminal() {
    which foot >/dev/null 2>&1 && yzconf set "terminal" "foot" && return
    which alacritty >/dev/null 2>&1 && yzconf set "terminal" "alacritty" && return
    which ghostty >/dev/null 2>&1 && yzconf set "terminal" "ghostty" && return
    which kitty >/dev/null 2>&1 && yzconf set "terminal" "kitty" && return
    term="$(choose 'Select terminal...' 'Alacritty' 'Foot' 'Ghostty' 'Kitty' 'I already have a terminal')"
    case "${term}" in
        "Alacritty") install_alacritty ;;
        "Foot") install_foot ;;
        "Ghostty") install_ghostty ;;
        "Kitty") install_kitty ;;
        "I already have a terminal") other_terminal ;;
    esac
}
