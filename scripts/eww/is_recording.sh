#!/usr/bin/env bash

if pidof wf-recorder; then
    eww update recorder_selected=0
else
    eww update recorder_selected=1
fi
echo ""
