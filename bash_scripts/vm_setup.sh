#!/bin/sh

# exit on errors
set -e
# check if not running as root
test "$UID" -gt 0 || { info "don't run this as root!"; exit; }
# ask for user password once, set timestamp. see sudo(8)
info "setting / verifying sudo timestamp"
# sudo -v




# save current working directory
workdir=$PWD

packages=("micro" "neofetch" "exa" "qemu-guest-agent")

# ----------------------------------
# Colors
# ----------------------------------
NOCOLOR='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
LIGHTGRAY='\033[0;37m'
DARKGRAY='\033[1;30m'
LIGHTRED='\033[1;31m'
LIGHTGREEN='\033[1;32m'
YELLOW='\033[1;33m'
LIGHTBLUE='\033[1;34m'
LIGHTPURPLE='\033[1;35m'
LIGHTCYAN='\033[1;36m'
WHITE='\033[1;37m'


function install_pkgs(){
    apt-get update  # To get the latest package lists
    for pkg in ${packages[@]};do
        if [[ $(command -v $pkg) ]]; then
            echo -e "${GREEN}$pkg is already installed${NOCOLOR}"

        else
            echo -e "${GREEN}Installing $pkg${NOCOLOR}"
            sudo apt install $pkg -qq
        fi
    done
}

# # You may want to put all your additions into a separate file like
# # ~/.bash_aliases, instead of adding them here directly.
# if [ -f ~/.bash_aliases ]; then
#     . ~/.bash_aliases
# fi

function edit_bash(){
    echo "alias ls='exa -la --icons --group-directories-first'" >>~/.bashrc

}


install_pkgs
edit_bash