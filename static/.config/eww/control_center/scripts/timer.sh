#!/usr/bin/env bash

n="$1"
((n=n+1))

mins=$((n/60))
secs=$((n-(60*mins)))

[ $mins -lt 10 ] && mins="0${mins}"
[ $secs -lt 10 ] && secs="0${secs}"

eww update mins="$mins"
eww update secs="$secs"