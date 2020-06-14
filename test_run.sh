#!/bin/bash

#use this for quickly testing code and config changes
#make sure to bump up version number and re-run setup.py before committing
sudo cp configs/justBoost.json /etc/pihud/pihud.json 
sudo python3 -m setup.py install 
sudo clear 
sudo python3 -m pihud
