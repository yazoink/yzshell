function install_intel() {
    clear
    pkgs=("linux-firmware-intel" "libvpl" "libvdpau-va-gl")
    a="$(gum choose --header 'Select Intel drivers...' 'Standard' 'Legacy (Gen 2-7)' 'Cancel')"
    case "${a}" in
        "Standard")
            pkgs+=(
                "mesa"
                "vulkan-intel"
                "intel-media-driver"
                "vpl-gpu-rt"
            )
            ;;
        "Legacy (Gen 2-7)")
            pkg_installed "mesa" && sudo pacman -Rns mesa
            if gum confirm "Install Vulkan drivers? (Gen 3+)"; then
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
    clear
    ! gum confirm "This script does not support < Rx 2000, continue?" && return
    pkgs=(
        "mesa"
        "libva-mesa-driver"
        "vulkan-radeon"
        "libvdpau-va-gl"
    )
    install_pkgs "${pkgs[@]}"
}

function install_gpu_drivers() {
    clear
    fm=$(gum choose --header 'Select graphics drivers...' "Intel" "AMD" "I will deal with graphics drivers")
    case "${fm}" in
        "Intel") install_intel ;;
        "AMD") install_amd ;;
    esac
}
