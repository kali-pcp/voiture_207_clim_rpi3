#!/bin/bash

echo setup interface
#modprobe can_raw
#modprobe can_dev
#insmod /home/pi/usb2can/usb_8dev.ko
#sudo ip link set can0 up type can bitrate 125000 sample-point 0.875
echo sender looper
### FAN
speed_fan="00"
temp_fan_LEFT="00"
temp_fan_RIGHT="00"
recycle_air_fan="00"
position_fan="00"
manuel_auto_pareprise_fan="00"

manuel_auto_pareprise_fan_data_send_2_fois_max=0
manuel_auto_pareprise_fan_data_send_1_fois_max_truc_avant=0

while [ True ]
do
    while read p; do

        if [[ ${p} == *"speed_fan"* ]];then
            speed_fan=$(echo ${p} | cut -d'=' -f2)
            if [[ ${manuel_auto_pareprise_fan} == "21" || ${manuel_auto_pareprise_fan} == "11" ]] && [[ ${speed_fan} == "0F" ]];then
                speed_fan=00
            fi
        fi

        if [[ ${p} == *"temp_fan_LEFT"* ]];then
            temp_fan_LEFT=$(echo ${p} | cut -d'=' -f2)
        fi

        if [[ ${p} == *"temp_fan_RIGHT"* ]];then
            temp_fan_RIGHT=$(echo ${p} | cut -d'=' -f2)
        fi

        if [[ ${p} == *"recycle_air_fan"* ]];then
            if [[ ${manuel_auto_pareprise_fan} != "21" && ${manuel_auto_pareprise_fan} != "11" ]];then
                recycle_air_fan=$(echo ${p} | cut -d'=' -f2)
            fi
        fi

        if [[ ${p} == *"position_fan"* ]];then
            if [[ ${manuel_auto_pareprise_fan} != "21" && ${manuel_auto_pareprise_fan} != "11" ]];then
                position_fan=$(echo ${p} | cut -d'=' -f2)
            fi
        fi

        if [[ ${p} == *"manuel_auto_pareprise_fan"* ]];then
            manuel_auto_pareprise_fan=$(echo ${p} | cut -d'=' -f2)

            if [[ ${manuel_auto_pareprise_fan} == "21" || ${manuel_auto_pareprise_fan} == "11" ]] && [[ ${speed_fan} == "0F" ]];then
                speed_fan=00
            fi


            if [[ ${manuel_auto_pareprise_fan} == 62 ]];then ### TRUC à l'arriere
                if [[ ${manuel_auto_pareprise_fan_data_send_2_fois_max} == 1 ]];then
                    manuel_auto_pareprise_fan_data_send_2_fois_max=0
                    sed -i 's/manuel_auto_pareprise_fan=62/manuel_auto_pareprise_fan=22/g' data.txt
                fi
                manuel_auto_pareprise_fan_data_send_2_fois_max=$(($manuel_auto_pareprise_fan_data_send_2_fois_max+1))
            fi
            
            if [[ ${manuel_auto_pareprise_fan} == "21" ]];then ### TRUC à l'avant
                echo ${manuel_auto_pareprise_fan_data_send_1_fois_max_truc_avant}
                if [[ ${manuel_auto_pareprise_fan_data_send_1_fois_max_truc_avant} == 1 ]];then
                    manuel_auto_pareprise_fan_data_send_1_fois_max_truc_avant=0
                    sed -i 's/manuel_auto_pareprise_fan=21/manuel_auto_pareprise_fan=11/g' data.txt
                fi
                manuel_auto_pareprise_fan_data_send_1_fois_max_truc_avant=$(($manuel_auto_pareprise_fan_data_send_1_fois_max_truc_avant+1))
                position_fan=10
                recycle_air_fan=10
            fi
            if [[ ${manuel_auto_pareprise_fan} == "11" ]];then ### TRUC à l'avant
                position_fan=10
                recycle_air_fan=10
            fi
        fi
    
    done < data.txt

    echo "1D0# ${manuel_auto_pareprise_fan} 00 ${speed_fan} ${position_fan} ${recycle_air_fan} ${temp_fan_LEFT} ${temp_fan_RIGHT}"   ### Send DATA TO CLIM
#    cansend can0 1D0#${manuel_auto_pareprise_fan}00${speed_fan}${position_fan}${recycle_air_fan}${temp_fan_LEFT}${temp_fan_RIGHT}
    #sleep 0.05s
done

