#!/bin/bash

# create venv if doesn't exist
if [ ! -d "/path/to/dir" ]; then
    python -m venv venv/
fi

# make sure all sources are up to date
source ./venv/bin/activate
pip install -r requirements.txt
