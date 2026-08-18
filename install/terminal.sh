function install_alacritty() {
    install_pkg "alacritty"
    yzconf set terminal alacritty
}

function install_foot() {
    install_pkg foot
    yzconf set terminal foot
}

function install_ghostty() {
    install_pkg ghostty
    yzconf set terminal ghostty
}

function other_terminal() {
    cmd=""
    while true; do
        read -p ">> Enter terminal command: " cmd
        answer_yes "Set '${cmd}' as terminal?" && break
    done
    yzconf set terminal "${cmd}"
}

function install_terminal() {
    which foot > /dev/null 2>&1 && yzconf set "terminal" "foot" && return
    which alacritty > /dev/null 2>&1 && yzconf set "terminal" "alacritty" && return
    term=""
    echo "
#### TERMINAL ####
1. alacritty
2. foot
3. ghostty
3. I already have a terminal"
    while true; do
        read -p ">> Install terminal [1-3]: " term
        [[ "${term}" =~ [1-4] ]] && break
    done
    case "$term" in
        "1") install_alacritty ;;
        "2") install_foot ;;
        "3") install_ghostty ;;
        "4") other_terminal ;;
    esac
}
