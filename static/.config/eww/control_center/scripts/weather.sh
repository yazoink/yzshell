#!/usr/bin/env bash

json="$(curl -s "https://api.open-meteo.com/v1/forecast?latitude=-37.814&longitude=144.9633&hourly=temperature_2m&current=temperature_2m,precipitation,cloud_cover,apparent_temperature,wind_speed_10m,is_day&timezone=auto&forecast_days=3"; [ $? -ne 0 ] && exit 1)"

# temp
temp=$(echo "$json" | jq ".current.temperature_2m")
unit=$(echo "$json" | jq ".current_units.temperature_2m" | sed 's/"//g')
#echo "${temp}${unit}"
eww update weather_temp="${temp}${unit}"

# apparent temp
temp=$(echo "$json" | jq ".current.apparent_temperature")
unit=$(echo "$json" | jq ".current_units.apparent_temperature" | sed 's/"//g')
#echo "Feels like ${temp}${unit}"
eww update weather_apparent_temp="Feels like ${temp}${unit}"

# icon
rain=$(echo "$json" | jq ".current.precipitation")
cloud=$(echo "$json" | jq ".current.cloud_cover")
is_day=$(echo "$json" | jq ".current.is_day")

i=""

if (( $(bc <<< "$rain > 0.1") )); then # rain
    if [ $is_day -eq 1 ]; then # day
        i=""
    else # night
        i=""
    fi
else # no rain
    if (( $(bc <<< "$cloud > 50") )); then # cloud
        if [ $is_day -eq 1 ]; then # day
            i=""
        else # night
            i=""
        fi
    else # no cloud
        if [ $is_day -eq 1 ]; then # day
            i=""
        else # night
            i=""
        fi
    fi
fi
eww update weather_icon="$i"

# colour
rain=$(echo "$json" | jq ".current.precipitation")
cloud=$(echo "$json" | jq ".current.cloud_cover")
is_day=$(echo "$json" | jq ".current.is_day")

c=""

if (( $(bc <<< "$rain > 0.1") )); then # rain
    c="base0D"
else # no rain
    if [ $is_day -eq 1 ]; then # day
        c="base0A"
    else # night
        c="base0D"
    fi
fi

eww update weather_colour="$c"

# timezone
tz=$(echo $json | jq ".timezone" | sed 's/"//g')
abv=$(echo $json | jq ".timezone_abbreviation" | sed 's/"//g')
eww update weather_tz="$tz ($abv)"
