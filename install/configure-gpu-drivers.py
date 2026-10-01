#!/usr/bin/env python

from utils import choose, install_pkgs, confirm, set_env_vars, remove_pkgs

c = choose("graphics drivers", ["amd", "intel", "none"])
match c:
    case "amd":
        if confirm("This script does not support < Rx 2000, continue?"):
            env_vars = {
                "LIBVA_DRIVER_NAME": "radeonsi",
                "VDPAU_DRIVER": "va_gl"
            }
            install_pkgs([
                "mesa", 
                "libva-mesa-driver", 
                "vulkan-radeon",
                "libvdpau-va-gl"
            ])
            set_env_vars(env_vars)
    case "intel":
        d = choose("intel drivers", ["standard", "legacy (gen 2-7)", "none"])
        match d:
            case "standard":
                env_vars = {
                    "LIBVA_DRIVER_NAME": "iHD",
                    "VDPAU_DRIVER": "va_gl"
                }
                install_pkgs([
                    "mesa",
                    "vulkan-intel",
                    "intel-media-driver",
                    "vpl-gpu-rt"
                ])
                set_env_vars(env_vars)
            case "legacy (gen 2-7)":
                env_vars = {
                    "LIBVA_DRIVER_NAME": "i965",
                    "VDPAU_DRIVER": "va_gl"
                }
                remove_pkgs(["mesa"])
                install_pkgs([
                    "mesa-amber",
                    "libva-intel-driver",
                    "intel-media-sdk"
                ])
                set_env_vars(env_vars)