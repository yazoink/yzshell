#!/usr/bin/env bash

if pidof wf-recorder; then
    echo '1'
else
    echo '0'
fi