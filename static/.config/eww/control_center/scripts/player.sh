#!/usr/bin/env bash

playerctl "$1"

case "$1" in
    "play-pause")
        eww update song_status="$(control_center/scripts/get_player_status.sh)"
        ;;
    "next" | "prev") 
        eww update song="$(playerctl metadata title | echo "n/a")"
        eww update song_artist="$(playerctl metadata artist | echo "n/a")"
        eww update cover_art="$(control_center/scripts/get_album_cover.sh)"
        ;;
esac