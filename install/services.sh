disable=("systemd-oomd.socket" "systemd-oomd")
enable=(
    "ananicy-cpp"
    "irqbalance"
    "memavaild"
    "nohang"
    "preload"
    "prelockd"
    "uresourced"
    "fstrim.timer"
    "swayosd-libinput-backend.service"
    "bluetooth.service"
)
enable_user=("mpd")

for s in "${disable[@]}"; do
    sudo systemctl disable --now "${s}"
done

for s in "${enable[@]}"; do
    sudo systemctl enable --now "${s}"
done

for s in "${enable_user[@]}"; do
    systemctl enable --user --now "${s}"
done