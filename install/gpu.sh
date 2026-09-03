function install_intel() {
    pkgs=("linux-firmware-intel" "libvpl" "libvdpau-va-gl")
    a="$(choose 'Select Intel drivers...' 'Standard' 'Legacy (Gen 2-7)' 'Cancel')"
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
            if confirm "Install Vulkan drivers? (Gen 3+)"; then
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
    ! confirm "This script does not support < Rx 2000, continue?" && return
    pkgs=(
        "mesa"
        "libva-mesa-driver"
        "vulkan-radeon"
        "libvdpau-va-gl"
    )
    install_pkgs "${pkgs[@]}"
}

function install_gpu_drivers() {
    fm=$(choose 'Select graphics drivers...' "Intel" "AMD" "I will deal with graphics drivers")
    case "${fm}" in
        "Intel") install_intel ;;
        "AMD") install_amd ;;
    esac
}
