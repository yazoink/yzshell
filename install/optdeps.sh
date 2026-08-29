OPT_DEPS=(
    "fastfetch"
    "gimp"
    "htop"
    "fastfetch"
    "galculator"
    "wf-recorder"
    "nicotine+"
    "prismlauncher"
    "tree"
    "keepassxc"
    "libreoffice-still"
    "pluma"
    "kruler"
    "qbittorrent"
    "yt-dlp"
    # nvim formatters
    "python-isort"
    "python-black"
    "prettier"
    "shfmt"
    "yamllint"
    "yamlfmt"
    "uncrustify"
    "typstyle"
    "stylua"
    #
    "xz"
    "p7zip"
    "tumbler"
    "android-tools"
    "ffmpegthumbnailer"
    "webp-pixbuf-loader"
    "poppler-glib"
    "libgsf"
    "gvfs"
    "gvfs-smb"
    "gvfs-mtp"
    "gvfs-gphoto2"
    "cryptsetup"
    "udisks2"
    "udiskie"
    "ntfsprogs"
    "wlr-randr"
    "nwg-displays"
)

OPT_AUR_DEPS=(
    # nvim formatters
    "alejandra"
    "beautysh"
    "mago-bin"
    #"pretty-php"
    #"fixjson"
)

function install_vscode() {
    extensions=(
        "pkief.material-icon-theme"
        "pkief.material-product-icons"
        "meta.pyrefly"
        "ms-python.python"
        "pinage404.bash-extension-pack"
        "eww-yuck.yuck"
        "devsense.phptools-vscode"
        "redhat.vscode-yaml"
        "redhat.vscode-xml"
        "ecmel.vscode-html-css"
        "yzhang.markdown-all-in-one"
        "tamasfe.even-better-toml"
        "sumneko.lua"
    )
    install_pkgs "code"
    for e in "${extensions[@]}"; do
        gum spin \
            --spinner dot \
            --title "Installing Vscodium extension '${e}'..." -- \
            code --install-extension "${e}"
    done
    announce "Vscodium installed!"
}

function install_dict() {
    if ! which dict >/dev/null 2>&1; then
        clear
        ! gum confirm "Install Dict (https://github.com/yazoink/dict)?" &&
        return 1
        curl -s https://raw.githubusercontent.com/yazoink/dict/refs/heads/main/dict >/tmp/dict
        sudo install -Dm755 /tmp/dict /usr/bin/dict
        rm /tmp/dict
        announce "Dict installed!"
    fi
}

function install_soundboard() {
    if ! which soundboard >/dev/null 2>&1; then
        clear
        ! gum confirm \
            "Install Soundboard (https://github.com/yazoink/soundboard)?" &&
        return 1
        deps=(
            "python"
            "python-gobject"
            "alsa-utils"
            "git"
        )
        install_pkgs "${deps[@]}"

        [ ! -d ~/src ] && mkdir -p ~/src
        gum spin \
            --spinner dot \
            --title "Downloading Soundboard..." -- \
            git clone https://github.com/yazoink/soundboard.git ~/src/soundboard
        sudo mkdir -p /usr/share/soundboard/
        sudo cp -rf ~/src/soundboard/sounds /usr/share/soundboard/sounds
        [ ! -d ~/.config/soundboard ] && mkdir -p ~/.config/soundboard
        cp ~/src/soundboard/config.json ~/.config/soundboard/config.json
        sudo install -Dm755 ~/src/soundboard/soundboard.py /usr/bin/soundboard
        echo "[Desktop Entry]
Name=Soundboard
Comment=play sounds and stuff
Exec=soundboard
Type=Application" | sudo tee /usr/share/applications/soundboard.desktop >/dev/null
        announce "Soundboard installed!"
    fi
}
