#!/bin/bash

# Github: mategol/PySilon-malware
# Author: Neek8044
# Description: Bash script to compile PySilon under Linux with wine

# Supported distros: Ubuntu, Fedora, Arch (and derivatives)
# Not supported: openSUSE, Nix, Void, Debian, Alpine, etc.

if [ $(whoami) = 'root' ]; then
    echo -e "\e[1;31mYou must not run this as root. Rerun without root.\e[0m"
    exit
fi

echo -e "[+] Configure Wine first? \e[32m[c]onfigure\e[0m/\e[31m[r]un anyways\e[0m (you must configure if it's the first time running this)"
read -p "$ " mode

# If configuration mode was selected, do these:
if [ $mode = 'c' ]; then
    # Ask if wine is installed
    echo -e "[+] Do you have wine already installed? \e[32m[y]es\e[0m/\e[31m[n]o\e[0m (defaults to yes)"
    read -p "$ " wine_installed
    # If wine is not installed, show prompt to choose package manager
    if [ $wine_installed = 'n' ]; then
        echo -e "[+] Select your package manager (\e[34m[a]pt\e[0m, \e[34m[d]nf\e[0m, \e[34m[p]acman\e[0m) or hit \e[34menter\e[0m to skip."
        read -p "$ " package_manager

        # Install wine using the selected package manager
        if [ $package_manager = 'a' ]; then
            sudo apt update -y && sudo apt install wine -y
        elif [ $package_manager = 'd' ]; then
            sudo dnf update -y && sudo dnf install wine -y
        elif [ $package_manager = 'p' ]; then
            sudo pacman -Sy wine --noconfirm
        else
            echo -e "\e[31m[x] Enter was pressed or invalid input was given, skipping.\e[0m"
        fi
    elif [ $wine_installed = 'y' ]; then
        :
    else
        echo -e "\e[31m[x] Enter was pressed or invalid input was given, skipping.\e[0m"
    fi

    # Ask to download and install Python in Wine
    echo -e "[+] Install Python inside of wine? \e[32m[y]es\e[0m/\e[34menter\e[0m to skip."
    read -p "$ " install_python

    # If user entered 'y', download and install Python in Wine
    if [ $install_python = 'y' ]; then
        echo -e "\e[36m[#] Fetching Python for Windows...\e[0m"
        wget https://www.python.org/ftp/python/3.10.8/python-3.10.8-amd64.exe # Change link for a different version (3.10.8 works fine under wine)
        echo -e "\e[36m[#] Launching Python installer through Wine...\e[0m"
        echo -e "\e[1;35m[i] Make sure to add Python to PATH in the installer!\e[0m"
        wine ./python-3.10.8-amd64.exe # Change version to the version set in the above link
    else
        echo -e "\e[31m[x] Enter was pressed or invalid input was given, skipping.\e[0m"
    fi

    # Install requirements.txt
    echo -e "\e[36m[#] Installing PIP requirements.txt...\e[0m"
    wine pip install wheel setuptools
    wine python -m pip install -r requirements.txt

# If run mode was selected, continue
elif [ $mode = 'r' ]; then
    :
# If no mode was selected, display error and continue
else
    echo -e "\e[31mInvalid input, proceeding to the execuion of builder.py anyways.\e[0m"
fi

# Running builder.py
echo -e "\e[36m[#] Running builder.py...\e[0m"
wine python builder.py

echo
echo -e "\e[33m#===============================================#\e[0m"
echo -e "\e[33m# Software terminated.                          #\e[0m"
echo -e "\e[33m#                                               #\e[0m"
echo -e "\e[33m# Give me a star on Github!                     #\e[0m"
echo -e "\e[33m# https://github.com/mategol/PySilon-malware    #\e[0m"
echo -e "\e[33m#===============================================#\e[0m"
echo
echo
