source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

export HISTFILE=~/.zsh_history
export HISTFILESIZE=100000

PROMPT="%n@%m~ "

copyfile() {
    cat "$1" | wl-copy
}

alias ls="ls --color=auto"
alias y="yazi"
alias add="sudo xbps-install"
alias del="sudo xbps-remove -o"
alias upd="sudo xbps-install -Su"
alias qry="xbps-query -Rs"
alias gcl="git clone"
alias gaa="git add ."
alias ga="git add"
alias gc="git commit -m"
alias gcm="git commit -m 'something'"
alias gps="git push"
alias chx="chmod +x"
alias cpdir="wl-copy \"$(pwd)\""
alias myip="curl http://ipecho.net/plain; echo"
alias mu="ncmpcpp"