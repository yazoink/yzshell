#!/usr/bin/env bash
i=""
if makoctl mode | grep -q do-not-disturb; then
    i=''
else
    i=''
fi

eww update dnd_icon="${i}"