#!/usr/bin/env bash

visible=0
pidof waybar && visible=1

if [ $visible == 1 ]; then
    yzshell module bar hide
else
    yzshell module bar show
fi
