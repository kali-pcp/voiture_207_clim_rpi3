#!/bin/bash
## CHOISIR DE Démarer sur l'app ou sur le bureau pour de la maintenance 
## executer en root


## Revenir au BUREAU
sudo sed -i 's/startx &/#startx &/g' /etc/rc.local 

sudo sed -i 's/exec openbox-session/#exec openbox-session/g' /etc/X11/xinit/xinitrc  
sudo sed -i 's+#. /etc/X11/Xsession+. /etc/X11/Xsession+g' /etc/X11/xinit/xinitrc

sudo sed -i 's+/bin/python3.7 /home/pi/Desktop/voiture_207_clim_rpi3/app.py &+#/bin/python3.7 /home/pi/Desktop/voiture_207_clim_rpi3/app.py &+g' /etc/xdg/openbox/autostart 
sudo raspi-config
sudo reboot

## REVENIR à l'app
#sudo sed -i 's/#startx &/startx &/g' /etc/rc.local 
sudo su
sudo sed -i '/#startx &/d' /etc/rc.local
sudo sed -i '/exit 0/d' /etc/rc.local
sudo echo "startx &" >> /etc/rc.local
sudo echo "exit 0" >> /etc/rc.local

sudo sed -i 's+#exec openbox-session+exec openbox-session+g' /etc/X11/xinit/xinitrc  
sudo sed -i 's+. /etc/X11/Xsession+#. /etc/X11/Xsession+g' /etc/X11/xinit/xinitrc

sudo echo "/bin/python3.7 /home/pi/Desktop/voiture_207_clim_rpi3/app.py &" > /etc/xdg/openbox/autostart

reboot now 
