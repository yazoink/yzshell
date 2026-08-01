#!/usr/bin/env bash

swayidle -w \
    timeout 300 'yzshell lock' \
    timeout 600 'hyprctl dispatch dpms off' \
    resume 'hyprctl dispatch dpms on' \
    before-sleep 'yzshell lock'