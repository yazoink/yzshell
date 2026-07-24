#!/usr/bin/env bash

if sensors | grep -q 'Core 0'; then
    sensors | grep 'Core 0' | awk '{print $3}' | sed 's/\+//g;s/\.[0-9]°C//g'
else
    sensors | grep Tctl | awk '{print $2}' | sed 's/\+//g;s/\.[0-9]°C//g'
fi