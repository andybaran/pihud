#!/bin/bash

echo "Pulling down python3 apt packages"
sudo apt-get install vim python3-pyqt5 python3-pip python3-yaml python3-rpi.gpio playerctl -y

echo "Doing pips for modules without packages"
pip3 install obd

echo "Cloning code from GitHub"
git clone https://github.com/Ircama/ELM327-emulator
git clone https://github.com/andybaran/pihud.git
git clone  https://github.com/andybaran/rpi-audio-receiver

