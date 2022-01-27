#!/bin/bash
#echo coucou > /home/pi/Desktop/ccc.txt
#startx
#sleep 10s





#ip link set wlan0 down
sudo screen -d -m /home/pi/Desktop/sender.sh
sudo screen -d -m /home/pi/Desktop/send_data_clim.sh
sudo screen -d -m /home/pi/Desktop/network.sh

#/bin/python3.7 /home/pi/Desktop/app.py

### Start Network
#systemctl start bt-agent@hci0.service
#systemctl start ssh.service
#systemctl start wpa_supplicant.service
#systemctl start pulseaudio.service
#systemctl start dhcpcd
#systemctl start systemd-timesyncd