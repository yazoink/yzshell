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
