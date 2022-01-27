# voiture_207_clim_rpi3



Disable Desktop autologin
Run sudo raspi-config and navigate to 3 Boot Options / B1 Desktop / Cliand choose B2 Console Autologin
Run startx in rc.local
Open rc.local with sudo nano /etc/rc.local. At the end, before exit 0 add startx &
Configure xinitrc
sudo nano /etc/X11/xinit/xinitrc
Comment this line

. /etc/X11/xsession
Add this line to start openbox

exec openbox-session
Run your programs with autostart
sudo nano /etc/xdg/openbox/autostart
Add your commands

/path/to/program &
Important: End all commands with &

