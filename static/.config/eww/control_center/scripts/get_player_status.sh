#!/bin/bash

status="$(playerctl status)"

if [ "$status" == "Paused" ]; then
    echo ""
elif [ "$status" == "Stopped" ]; then
    echo ""
else
    echo ""
fi