function install_alacritty() {
    install_pkg "alacritty"
    yzconf set terminal alacritty
}

function install_foot() {
    install_pkg foot
    yzconf set terminal thunar
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
    which foot > /dev/null && yzconf set "terminal" "foot" && return
    which alacritty > /dev/null && yzconf set "terminal" "alacritty" && return
    term=""
    echo "
#### TERMINAL ####
1. alacritty
2. foot
3. I already have a terminal"
    while true; do
        read -p ">> Install terminal [1-3]: " term
        [[ "${term}" =~ [1-3] ]] && break
    done
    case "$term" in
        "1") install_alacritty ;;
        "2") install_foot ;;
        "3") other_terminal ;;
    esac
}
