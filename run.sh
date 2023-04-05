#!/bin/bash

BASE_DIR=$(pwd)
# make sure we're in the virtual environment
source $BASE_DIR/venv/bin/activate

# start the server
echo -e "\nStarting the server..."
export PYTHONPATH="$PYTHONPATH:$BASE_DIR"
python $BASE_DIR/src/soundboi.py
