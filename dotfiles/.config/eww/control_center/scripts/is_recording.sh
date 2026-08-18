#!/usr/bin/env bash

if pidof wf-recorder; then
    eww update recorder_selected=0
    echo 'true'
else
    eww update recorder_selected=1
    echo 'false'
fi