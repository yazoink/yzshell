#!/usr/bin/env bash

family="${1}"

current="$(yzconf get "${family}"_font)"
eww update current_font="${current}"
