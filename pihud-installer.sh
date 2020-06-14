#!/bin/bash

echo "Pulling down python3 apt packages"
sudo apt-get install vim python3-pyqt5 python3-pip python3-yaml python3-rpi.gpio -y

echo "Installing PySide2"
apt-get install python3-pyside2.qt3dcore python3-pyside2.qt3dinput python3-pyside2.qt3dlogic python3-pyside2.qt3drender python3-pyside2.qtcharts python3-pyside2.qtconcurrent python3-pyside2.qtcore python3-pyside2.qtgui python3-pyside2.qthelp python3-pyside2.qtlocation python3-pyside2.qtmultimedia python3-pyside2.qtmultimediawidgets python3-pyside2.qtnetwork python3-pyside2.qtopengl python3-pyside2.qtpositioning python3-pyside2.qtprintsupport python3-pyside2.qtqml python3-pyside2.qtquick python3-pyside2.qtquickwidgets python3-pyside2.qtscript python3-pyside2.qtscripttools python3-pyside2.qtsensors python3-pyside2.qtsql python3-pyside2.qtsvg python3-pyside2.qttest python3-pyside2.qttexttospeech python3-pyside2.qtuitools python3-pyside2.qtwebchannel python3-pyside2.qtwebsockets python3-pyside2.qtwidgets python3-pyside2.qtx11extras python3-pyside2.qtxml python3-pyside2.qtxmlpatterns python3-pyside2uic qt5-qmltooling-plugins python-pyside2-doc fonts-roboto

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
