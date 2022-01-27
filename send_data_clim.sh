#!/bin/bash

echo setup interface
modprobe can_raw
modprobe can_dev
insmod /home/pi/usb2can/usb_8dev.ko
sudo ip link set can0 up type can bitrate 125000 sample-point 0.875
#cansend can0 1D0#${manuel_auto_pareprise_fan}00${speed_fan}${position_fan}${recycle_air_fan}${temp_fan_LEFT}${temp_fan_RIGHT}
canoutput="/home/pi/Desktop/can_data_clim.txt"
while [ True ]
do
    cansend can0 $(echo $(cat ${canoutput}))
    echo cansend can0 $(echo $(cat ${canoutput}))
    #sleep 0.02s
done
