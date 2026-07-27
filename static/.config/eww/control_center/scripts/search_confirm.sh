#!/usr/bin/env bash

yzshell close_all_widgets &

selected=$(eww get search_selected)
if [ $selected -gt -1 ]; then
    # get launch command of selected app
    c="$(eww get search_results \
        | jq -r ".[${selected}].cmd")"
    (
        cd "$HOME" || exit
        eval "$c" & disown
    )
fi