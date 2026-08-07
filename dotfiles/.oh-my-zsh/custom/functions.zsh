function extr() {
	for archive in "$@"; do
		if [ -f "$archive" ] ; then
			case $archive in
				*.tar.bz2)   tar xvjf $archive    ;;
				*.tar.gz)    tar xvzf $archive    ;;
				*.bz2)       bunzip2 $archive     ;;
				*.rar)       rar x $archive       ;;
				*.gz)        gunzip $archive      ;;
				*.tar)       tar xvf $archive     ;;
				*.tbz2)      tar xvjf $archive    ;;
				*.tgz)       tar xvzf $archive    ;;
				*.zip)       unzip $archive       ;;
				*.Z)         uncompress $archive  ;;
				*.7z)        7z x $archive        ;;
				*)           echo "don't know how to extract '$archive'..." ;;
			esac
		else
			echo "'$archive' is not a valid file!"
		fi
	done
}

function copyfile() {
    cat "$1" | wl-copy
}

function mkcd() {
    mkdir -p "$1" && cd "$1"
}

function bckup() {
    cp -r "$1" "$1.backup.$(date +%Y%m%d_%H%M%S)"
    echo "Backed up to $1.backup.$(date +%Y%m%d_%H%M%S)"
}

function y() {
	local tmp="$(mktemp -t "yazi-cwd.XXXXXX")" cwd
	command yazi "$@" --cwd-file="$tmp"
	IFS= read -r -d '' cwd < "$tmp"
	[ "$cwd" != "$PWD" ] && [ -d "$cwd" ] && builtin cd -- "$cwd"
	command rm -f -- "$tmp"
}

function add() {
	sudo pacman -S --needed "$1"
	yzwidgets ctl control_center_update_all_apps
}

function auradd() {
	yay -S --needed "$1"
	yzwidgets ctl control_center_update_all_apps
}

function del() {
	sudo pacman -Rns "$1"
	yzwidgets ctl control_center_update_all_apps
}

function aurdel() {
	yay -Rns "$1"
	yzwidgets ctl control_center_update_all_apps
}