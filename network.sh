#!/bin/bash
sudo systemctl start networking.service
sudo systemctl start wpa_supplicant.service 
sudo systemctl start ssh.service 
sudo systemctl start dhcpcd