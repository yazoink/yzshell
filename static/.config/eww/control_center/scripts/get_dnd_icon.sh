#!/usr/bin/env bash

mode="$(makoctl mode)"
if [[ "$mode" == *"do-not-disturb"* ]]; then
    eww update dnd_icon=""
else
    eww update dnd_icon=""
fi
