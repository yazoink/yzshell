#!/bin/bash
# stolen from https://github.com/GuyWithXM5/PulseDock/blob/main/scripts/get-cover.sh
# Downloads cover art from the MPRIS artUrl and outputs the local file path.
PLAYER="chromium,chrome,firefox,brave,%any"
COVER_DIR="/tmp/eww-music-cover"
mkdir -p "$COVER_DIR"

URL=$(playerctl --player="$PLAYER" metadata mpris:artUrl 2>/dev/null)
if [ -z "$URL" ]; then
    echo ""
    exit 0
fi

# Cache by URL hash to avoid redundant downloads
HASH=$(echo "$URL" | md5sum | cut -d' ' -f1)
CACHED="$COVER_DIR/${HASH}.jpg"

if [ ! -f "$CACHED" ]; then
    # Remove old covers before saving the new one
    rm -f "$COVER_DIR"/*.jpg 2>/dev/null
    curl -s -L -o "$CACHED" "$URL" 2>/dev/null
fi

echo "$CACHED"