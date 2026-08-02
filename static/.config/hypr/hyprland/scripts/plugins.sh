#!/usr/bin/env bash

UPDATE_LOG_FILE="/tmp/hyprpm_1.log"
ADD_LOG_FILE="/tmp/hyprpm_2.log"

declare -A plugins
plugins["hyprbars"]="https://github.com/hyprwm/hyprland-plugins"

if [ -f "/tmp/hyprland_fresh_install" ]; then
    notify-send "Hyprpm" "Updating plugins..."
    o="$(hyprpm update)"
    r=$?
    echo "$o" > "$UPDATE_LOG_FILE"
    if [ $r -ne 0 ]; then
        notify-send --urgency=critical "Hyprpm" \
            "Update failed! See '${UPDATE_LOG_FILE}' for details"
        exit 1
    fi
    notify-send "Hyprpm" "Update complete - see '${UPDATE_LOG_FILE}' for details"
    for p in "${!plugins[@]}"; do
        if ! hyprpm list | grep -q "$p"; then
            notify-send "Hyprpm" "Adding repo '${plugins[p]}'..."
            o="$(hyprpm add "${plugins[p]}")"
            r=$?
            echo "$r" > "$ADD_LOG_FILE"
            if [ $r -ne 0 ]; then
                notify-send  --urgency=critical "Hyprpm" \
                    "Failed to add repo '${plugins[p]}'! See '${ADD_LOG_FILE}' for details"
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
fi

hyprpm reload
