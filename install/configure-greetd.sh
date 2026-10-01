#!/usr/bin/env bash

sudo mv /etc/greetd/config.toml /etc/greetd/config.toml.bak

echo "
[terminal]
vt = 1

[default_session]
command = \"agreety --cmd start-hyprland\"
user = \"greeter\"

[initial_session]
command = \"start-hyprland\"
user = \"$(whoami)\"" | sudo tee /etc/greetd/config.toml