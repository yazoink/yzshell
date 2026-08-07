#!/usr/bin/env bash

mode="$(makoctl mode)"

if makoctl mode | grep -q do-not-disturb; then
    echo ''
else
    echo ''
fi
