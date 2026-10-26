#!/usr/bin/env bash

hyprlock
yzshell
nm-applet &
wl-paste --watch cliphist store &
poweralertd &
udiskie &
hypridle &
wayland-pipewire-idle-inhibit &
/usr/lib/mate-polkit/polkit-mate-authentication-agent-1 &
if ! hyprpm list | grep -q hyprbars; then
    echo ">> Installing Hyprland plugins..."
    terminal="$(yzconf get terminal)"
    (
        sleep 5
        $terminal -e yzshell-install-hyprland-plugins &
    ) &
    disown
else
    hyprpm reload
fi
