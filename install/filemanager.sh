function install_pcmanfm() {
    pkgs=("pcmanfm" "file-roller")
    install_pkgs "${pkgs[@]}"
    yzconf set file_manager pcmanfm
}

function install_thunar() {
    pkgs=(
        "thunar"
        "thunar-archive-plugin"
        "thunar-media-tags-plugin"
        "thunar-shares-plugin"
        "file-roller"
    )
    install_pkgs "${pkgs[@]}"
    yzconf set file_manager thunar
}

function other_file_manager() {
    cmd=""
    while true; do
        cmd="$(input 'Enter file manager command...')"
        confirm "Set '${cmd}' as file manager?" && break
    done
    yzconf set file_manager "${cmd}"
}

function install_file_manager() {
    which thunar >/dev/null 2>&1 && yzconf set "file_manager" "thunar" && return
    which pcmanfm >/dev/null 2>&1 && yzconf set "file_manager" "pcmanfm" && return
    fm="$(choose 'Select file manager...' 'PCManFM' 'Thunar' 'I already have a file manager')"
    case "$fm" in
        "PCManFM") install_pcmanfm ;;
        "Thunar") install_thunar ;;
        "I already have a file manager") other_file_manager ;;
    esac
}
