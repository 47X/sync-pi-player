#!/bin/bash
#User autorun script invoked from .bashrc on main tty, run as as user pi
reset
cd /home/pi/sync-pi-player
echo ___________________________________________________
echo
echo SYNC-PI-PLAYER
echo "(c) 2017 Aleksander Janas, o@kilku.com"
echo Version: $(git log master |grep commit | wc -l)
echo Current software repository version:
git show --pretty=medium --abbrev-commit |head -n 3
echo ___________________________________________________
echo
echo Press NEXT to skip, press PLAY in 15 seconds to check for connection and updates, must be powered on during update!
read -rs -n1 -t15 keypressed
if [[ $keypressed = p ]]
  then
    echo
    echo Checking for internet connection...
    if wget -q --tries=10 --timeout=20 --spider http://github.com
      then
        echo Connected, checking for updates ....
        echo Version on server: $(git log origin/master |grep commit | wc -l)
        sudo mount -o remount,rw / ; sudo mount -o remount,rw /boot
        git pull
        sudo mount -o remount,ro / ; sudo mount -o remount,ro /boot
        echo ___________________________________________________
        echo ___________________________________________________
        echo Version: $(git log master |grep commit | wc -l)
        echo
        echo DO NOT UNPLUG POWER NOW! Press PLAY or NEXT to reboot...
        read -rsn1
        echo Rebooting now
        sudo reboot
      else
        echo "Internet connection failed :("
    fi
    echo Press PLAY or NEXT to continue...
    read -rsn1
fi

#initialize autossh reverse tunnel for remote access
#autossh -M 0 -q -f -N -o "ServerAliveInterval 60" -o "ServerAliveCountMax 3" -R $(cat /mnt/pen/PORT):localhost:22 pi@aruba


#exit 0
#cycle hdmi power to get black screen under video
tvservice -o
tvservice -p
sleep 3

#run player in screen and log to usb storage
sudo screen -L /mnt/pen/logfile -dmS klient "/home/pi/sync-pi-player/pi/player.py"



#getty tty
#screen -L /mnt/pen/logfile -dmS klient "/home/pi/BUTTONPLAYER/player.py"
#screen -r

#sudo /home/pi/BUTTONPLAYER/player.py
