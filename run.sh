#!/bin/bash

# make sure we're in the virtual environment, and pip files are up to date
source ./setup.sh

# start the server
echo -e "\nStarting the server...\n"
python ./soundboi.py
