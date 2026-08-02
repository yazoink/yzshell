#!/usr/bin/env bash

function fresh_install() {
    declare -A plugins
    plugins["hyprbars"]="https://github.com/hyprwm/hyprland-plugins"
    plugins["hyprexpo"]="https://github.com/sandwichfarm/hyprexpo"
    notify-send "Hyprpm" "Updating plugins..."
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
            notify-send "Hyprpm" "Adding repo '${plugins[p]}'..."
            hyprpm add "${plugins[p]}"
            r=$?
            if [ $r -ne 0 ]; then
                notify-send  --urgency=critical "Hyprpm" \
                    "Failed to add repo '${plugins[p]}'!"
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
}

if [ -f "/tmp/hyprland_fresh_install" ]; then
    fresh_install && rm -rf /tmp/hyprland_fresh_install
fi

hyprpm reload