#!/usr/bin/env bash

module="${1}"
val=$2

if [[ $(yzconf get bar_show_"${module}") != $val ]]; then
    eww update bar_show_"${module}"=$val
    yzconf set bar_show_"${module}" "${val}"
    yzconf deploy_configs -r -s
    yzshell reload bar
fi