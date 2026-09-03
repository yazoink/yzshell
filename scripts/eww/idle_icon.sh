#!/usr/bin/env bash

i=""

if pgrep --quiet hypridle; then
    i=""
else
    i=""
fi

eww update idle_icon="${i}"