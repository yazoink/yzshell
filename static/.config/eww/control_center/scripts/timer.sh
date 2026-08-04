#!/usr/bin/env bash

n="$(eww get timer)"
((n=n+1))

mins=$((n/60))
secs=$((n-(60*mins)))

[ $mins -lt 10 ] && mins="0${mins}"
[ $secs -lt 10 ] && secs="0${secs}"

echo "$n"
eww update mins="$mins"
eww update secs="$secs"