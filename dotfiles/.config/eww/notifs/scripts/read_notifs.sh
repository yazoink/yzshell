#!/usr/bin/env bash

cache_file=/tmp/notifs.json
expired_cache_file=/tmp/expired_notifs.json
timeout=5000

# $1: notif id
# $2: timeout
function timeout_notif() {
    sleep $2
    n="$(tail -n 1 $cache_file | jq -c --argjson p "$1" '.[] | select(.id == $p)')"
    tail -n 1 $expired_cache_file \
        | jq -c --argjson p "$n" '. += [$p]' >> $expired_cache_file
    delete_notif $1
}

# $1: notif id
# $2: expired?
function delete_notif() {
    file=$cache_file
    [ "$2" == "--expired" ] && file=$expired_cache_file
    tail -n 1 $file | jq -c --argjson p "$1" 'del(.[] | select(.id == $p))' >> $file
}

case "$1" in
    "delete") delete_notif $2 $3; exit 0 ;;
esac

echo "[]" > $cache_file
echo "[]" > $expired_cache_file

eww --no-daemonize open notifs
eww --no-daemonize open notification_center
killall tiramisu >/dev/null 2>&1
killall mako >/dev/null 2>&1
i=0
tiramisu -j | while read -r line; do
    l="$line"
    icon="$(echo $l | jq -r '.hints["image-path"]')"
    [ ! -f $icon ] && icon="$(iconfetch $icon)"
    l="$(echo "$l" \
        | jq -c ".icon = \"$icon\"")"
    tail -n 1 $cache_file \
        | jq -c --argjson p "$l" '. += [$p]' \
        | jq -c --argjson p "$i" '.[-1].id = $p' >> $cache_file
    t=$(echo "$line" | jq '.timeout')
    [ $t -eq -1 ] && t=$timeout
    t_ms=`echo "scale=2;${t}/1000" | bc`
    timeout_notif "$i" "$t_ms" & disown
    ((i=i+1))
done