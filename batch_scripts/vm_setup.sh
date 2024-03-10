#!/bin/sh

packages=("micro" "neofetch" "git" "exa" "qemu-guest-agent")

apt-get update  # To get the latest package lists
apt-get install <package name> -y
#etc.

# check if not running as root
test "$UID" -gt 0 || { info "don't run this as root!"; exit; }

function pac_install_pkg(){
    for pkg in ${packages[@]};do
        if [[ $(command -v $pkg) ]]; then
            echo -e "${GREEN}$pkg is already installed${NOCOLOR}"

        else
            echo -e "${GREEN}Installing $pkg${NOCOLOR}"
            sudo pacman -S $pkg --noconfirm --noprogressbar
        fi
    done
}