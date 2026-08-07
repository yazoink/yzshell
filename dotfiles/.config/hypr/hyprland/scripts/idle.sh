#!/usr/bin/env bash

swayidle -w \
    timeout 300 'hyprlock --grace 30' \
    timeout 600 'hyprctl dispatch dpms off' \
    resume 'hyprctl dispatch dpms on' \
    before-sleep 'hyprlock --grace 30'