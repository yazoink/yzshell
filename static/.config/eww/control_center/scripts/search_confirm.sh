#!/usr/bin/env bash

selected=$(eww get search_selected)
if [ $selected -gt -1 ]; then
    # get launch command of selected app
    c="$(eww get search_results \
        | jq -r ".[${selected}].cmd")"
    (cd "$HOME"; eval $c) & disown
fi

yzshell close control_center
