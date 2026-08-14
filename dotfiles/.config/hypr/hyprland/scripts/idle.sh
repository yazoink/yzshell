#!/usr/bin/env bash

swayidle -w \
    timeout 300 'hyprlock --grace 30' \
    timeout 600 "hyprctl dispatch 'hl.dsp.dpms({ action = \"disable\" })'" \
    resume "hyprctl dispatch 'hl.dsp.dpms({ action = \"enable\" })'" \
    before-sleep 'hyprlock --grace 30'
