#!/bin/bash

sudo cp ../soundboi_server.service /etc/systemd/system/
sudo systemctl enable soundboi_server
