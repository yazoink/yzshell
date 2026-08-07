#!/usr/bin/env bash

function fresh_install() {
    declare -A plugins
    plugins["hyprbars"]="https://github.com/hyprwm/hyprland-plugins"
    #plugins["hyprexpo"]="https://github.com/sandwichfarm/hyprexpo"
    notify-send "Hyprpm" "Installing plugins, please be patient..."
    hyprpm update
    r=$?
    if [ $r -ne 0 ]; then
        notify-send --urgency=critical "Hyprpm" \
            "Update failed!"
        exit 1
    fi
    notify-send "Hyprpm" "Update complete"
    for p in "${!plugins[@]}"; do
        if ! hyprpm list | grep -q "$p"; then
            notify-send "Hyprpm" "Adding repo '${plugins[$p]}'..."
            echo "${plugins[$p]}"
            echo $p
            echo y | hyprpm add "${plugins[$p]}"
            r=$?
            if [ $r -ne 0 ]; then
                notify-send  --urgency=critical "Hyprpm" \
                    "Failed to add repo '${plugins[$p]}'!"
                exit 1
            fi
        fi
        hyprpm enable "$p"
        if [ $? -ne 0 ]; then
            notify-send "Hyprpm" --urgency=critical "Failed enable plugin'${p}'!"
            exit 1
        fi
        notify-send "Hyprpm" "Enabled plugin '${p}'"
    done
    notify-send "Hyprpm" "All plugins installed"
    return 0
}

if [ -f "/tmp/hyprland_fresh_install" ]; then
    fresh_install && rm -rf /tmp/hyprland_fresh_install
fi

hyprpm reload