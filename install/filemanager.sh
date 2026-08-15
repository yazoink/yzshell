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
        read -p ">> Enter file manager command: " cmd
        answer_yes "Set '${cmd}' as file manager?" && break
    done
    yzconf set file_manager "${cmd}"
}

function install_file_manager() {
    which thunar > /dev/null && yzconf set "file_manager" "thunar" && return
    which pcmanfm > /dev/null && yzconf set "file_manager" "pcmanfm" && return
    fm=""
    echo "
#### FILE MANAGER ####
1. pcmanfm
2. thunar
3. I already have a file manager"
    while true; do
        read -p ">> Install file manager [1-3]: " fm
        [[ "${fm}" =~ [1-3] ]] && break
    done
    case "$fm" in
        "1") install_pcmanfm ;;
        "2") install_thunar ;;
        "3") other_file_manager ;; 
    esac
}