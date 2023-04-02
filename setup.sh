#!/bin/bash

# exit if anything fails below
set -e
clear

# install the apt-get installs up front
echo "Installing apt-get packages"
sudo apt-get -y install python3-venv ffmpeg

# create venv if doesn't exist
if [ ! -d "./venv/" ]; then
    echo -e "\nInstalling a virtual environment, since it doesn't exist"
    python -m venv ./venv/
fi

# make sure all sources are up to date
echo -e "\nUsing the virtual environment, and checking installs"
source ./venv/bin/activate
pip install -r requirements.txt

echo -e "\nSetup done!\n"
