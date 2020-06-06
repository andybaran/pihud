#!/bin/bash

echo "Pulling down python3 apt packages"
sudo apt-get install vim python3-pyqt5 python3-pip python3-yaml python3-rpi.gpio -y

echo "Doing pips for modules without packages"
pip3 install obd pyserial pyserial-asyncio

echo "Cloning code from GitHub"
git clone https://github.com/Ircama/ELM327-emulator
#git clone https://github.com/andybaran/pihud.git
git clone  https://github.com/andybaran/rpi-audio-receiver

echo "Setup systemd"
cp ./configs/systemd/pihud.service /lib/systemd/system/pihud.service
systemctl daemon-reload
systemctl enable pihud.service
systemctl start pihud.service
