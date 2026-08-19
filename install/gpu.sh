function install_intel() {
    a=""
    pkgs=("linux-firmware-intel" "libvpl" "libvdpau-va-gl")
    echo "
#### INTEL DRIVERS ####
1. Standard
2. Legacy (Gen 2-7)
3. Cancel"
    while true; do
        read -p ">> Select drivers [1-3]: " a
        [[ "${a}" =~ [1-3] ]] && break
    done
    case "${a}" in
        "1")
            pkgs+=(
                "mesa"
                "vulkan-intel"
                "intel-media-driver"
                "vpl-gpu-rt"
            )
            ;;
        "2")
            pkg_installed "mesa" && sudo pacman -Rns mesa
            if answer_yes "Install Vulkan drivers? (Gen 3+)"; then
                pkgs+=("vulkan-intel")
            fi
            pkgs+=(
                "mesa-amber"
                "libva-intel-driver"
                "intel-media-sdk"
            )
            ;;
        "3") return ;;
    esac
    install_pkgs "${pkgs[@]}"
}

function install_amd() {
    ! answer_yes "This script does not support < Rx 2000, continue?" && return
    pkgs=(
        "mesa"
        "libva-mesa-driver"
        "vulkan-radeon"
        "libvdpau-va-gl"
    )
    install_pkgs "${pkgs[@]}"
}

function install_gpu_drivers() {
    fm=""
    echo "
#### GRAPHICS DRIVERS ####
1. Intel
2. AMD
3. I will deal with graphics drivers"
    while true; do
        read -p ">> Install graphics drivers [1-3]: " fm
        [[ "${fm}" =~ [1-3] ]] && break
    done
    case "${fm}" in
        "1") install_intel ;;
        "2") install_amd ;;
    esac
}
