#!/bin/bash

# Github: mategol/PySilon-malware
# Author: Neek8044
# Description: Bash script to compile PySilon under Linux with wine

# Supported distros: Ubuntu, Fedora, Arch (and derivatives)
# Not supported: openSUSE, Nix, Void, Debian, Alpine, etc.

if [ $(whoami) = 'root' ]; then
	echo -e "[+] Select your package manager (\e[34m[a]pt\e[0m, \e[34m[d]nf\e[0m, \e[34m[p]acman\e[0m) or hit \e[34menter\e[0m to skip: "
    read -p "$ " package_manager
else
    echo -e "\e[31m[!] Rerun as root user.\e[0m"
    exit
fi

if [ $package_manager = 'a' ]; then
    sudo apt update -y && sudo apt install wine -y
elif [ $package_manager = 'd' ]; then
    sudo dnf update -y && sudo dnf install wine -y
elif [ $package_manager = 'p' ]; then
    sudo pacman -Sy wine --noconfirm
else
    echo -e "\e[31m[x] Enter press or invalid input, skipping.\e[0m"
fi

echo -e "[+] Install Python inside of wine? \e[32m[y]es\e[0m/\e[31m[n]o\e[0m"
read -p "$ " install_python

if [ $install_python = 'y' ]; then
    echo -e "\e[36m[#] Fetching Python 3.11.3 for Windows...\e[0m"
    wget https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe
    echo -e "\e[36m[#] Launching Python installer through Wine...\e[0m"
    echo -e "\e[35m[i] Make sure to add Python to PATH in the installer!\e[0m"
    wine ./python-3.11.3-amd64.exe
fi

echo -e "\e[36m[#] Installing PIP requirements...\e[0m"
wine python -m pip install -r requirements.txt
echo -e "\e[36m[#] Running compiler.py\e[0m"
wine python compiler.py
