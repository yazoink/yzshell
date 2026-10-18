#!/usr/bin/env bash

family="${1}"
font="${2}"
old="$(yzconf get "${family}"_font)"

[ "${old}" = "${font}" ] && exit 0

yzwidgets close all
yzconf set "${family}"_font "${font}"
yzconf deploy_configs -r -s
fc-cache -fv &
yzshell reload
notify-send "Font changed!" "You may need to log out and in again to fully apply changes." &
yzwidgets open settings