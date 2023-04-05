#!/bin/bash

# exit if anything fails below
set -e
BASE_DIR=$(pwd)

# install the apt-get installs up front
echo -e "Installing apt-get packages"
sudo apt-get -y install python3-venv ffmpeg

# create venv if doesn't exist
if [ ! -d "./venv/" ]; then
    echo -e "\nInstalling a virtual environment, since it doesn't exist"
    python -m venv $BASE_DIR/venv/
fi

# make sure all sources are up to date
echo -e "\nUsing the virtual environment, and checking installs"
source $BASE_DIR/venv/bin/activate

pip install -r $BASE_DIR/requirements.txt

echo -e "\nSetup done!\n"
