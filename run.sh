#!/bin/bash

# make sure we're in the virtual environment, and pip files are up to date
source ./scripts/setup.sh

# start the server
echo -e "\nStarting the server...\n"
python ./src/soundboi.py
