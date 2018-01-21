#!/usr/bin/env python3

from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import os
import sys
import RPi.GPIO as GPIO
import keyboard #pip3 install keyboard
import logging
logging.basicConfig(level=logging.INFO)

# # GPIO setup
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

preroll = (300.0 / 1000.0)

# playlists
videos = []
duration_files = []
durations = []
folder = "/mnt/pen/MJPG480/"

# find videos
for file in os.listdir(folder):
    if file.endswith('.mjpeg'):
        filepath = os.path.join(folder, file)
        videos.append(filepath)
videos.sort()

# find carfiles
for file in os.listdir(folder):
    if file.endswith('.duration'):
        filepath = os.path.join(folder, file)
        duration_files.append(filepath)
duration_files.sort()

# load durations
for file in duration_files:
    with open(file,'r') as f:
        r = f.readline()
        r = r.replace('\n', '').replace(' ', '').replace('\r', '')
        durations.append(float(r))

print('_________________')
print("found video files" + str(videos))
print('_________________')
print("found duration files " + str(duration_files))
print('_________________')
print("read durations " + str(durations))


videoIndex = 0
durationIndex = 0
videoFile = videos[videoIndex]

# gpio callbacks
def playcb(channel):
    if player.is_playing():
        print('rewinding')
        player.set_position(0.00)
        sleep(preroll)
        player.pause()
    else:
        print('play')
        player.play()
        player.set_position(0.00)


def nextcb(channel):
    global videoIndex
    global durationIndex
    videoIndex = (videoIndex + 1) % len(videos)
    durationIndex = (durationIndex + 1) % len(durations)
    videoFile = videos[videoIndex]
    print('loading ' + videoFile)
    os.popen("tvservice -o")
    player.load(videoFile)
    os.popen("tvservice -p")
    player.set_aspect_mode('stretch')
    player.set_position(0.00)
    sleep(preroll)
    player.pause()
    print('ready')

# wait for dbus
def waitfor(pl):
    while not pl.can_control():
        pass
    # sleep(0.1)


# # gpio event setup, uncomment for gpio
# GPIO.add_event_detect(13, GPIO.RISING, bouncetime=300)
# GPIO.add_event_detect(21, GPIO.RISING, bouncetime=300)
# GPIO.add_event_callback(21, playcb)
# GPIO.add_event_callback(13, nextcb)

# keyboard setup
keyboard.add_hotkey('p', lambda: playcb(21))
keyboard.add_hotkey('n', lambda: nextcb(13))

# start player
print('loading ' + videoFile + ' duration ' + str(durations[durationIndex]))
player = OMXPlayer(videoFile, args=['--loop'],
                   dbus_name='org.mpris.MediaPlayer2.omxplayer1')

sleep(5)
print(player.position())
player.set_aspect_mode('stretch')
player.set_position(0.00)
# print(player.position())
# player.seek(10)
sleep(preroll)
# print(player.position())
player.pause()
# player.action(16)
print('ready')


# main
try:
    while True:
        # check if currently playing clip is ending soon, if yes load next
        sleep(0.5)
        # try-except because it happens that this is executed when clips are reloading and no player instance present
        try:
            if player.can_control():
                if player.position() > (durations[durationIndex] - 1):
                    print('auto next after playback')
                    nextcb(0)
        except:
            print('.')
        # do nothing
        pass


# cleanup
except KeyboardInterrupt:
    # GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    player.quit()
