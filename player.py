#!/usr/bin/env python3

from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import os
import sys
import RPi.GPIO as GPIO
#import logging
# logging.basicConfig(level=logging.INFO)


# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

preroll = (300.0 / 1000.0)

videos = []
duration_files = []
durations = []
folder = "/mnt/pen/MJPG480/"

for file in os.listdir(folder):
    if file.endswith('.mjpeg'):
        filepath = os.path.join(folder, file)
        videos.append(filepath)

for file in os.listdir(folder):
    if file.endswith('.duration'):
        filepath = os.path.join(folder, file)
        duration_files.append(filepath)

for file in duration_files:
    with open(file,'r') as f:
        r = f.readline()
        r = r.replace('\n', '').replace(' ', '').replace('\r', '')
        durations.append(float(r))

videos.sort()
duration_files.sort()
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
    player.load(videoFile)
    player.set_aspect_mode('stretch')
    player.set_position(0.00)
    sleep(preroll)
    player.pause()
    print('ready')


def waitfor(pl):
    while not pl.can_control():
        pass
    # sleep(0.1)


# gpio event setup
GPIO.add_event_detect(13, GPIO.RISING, bouncetime=300)
GPIO.add_event_detect(21, GPIO.RISING, bouncetime=300)
GPIO.add_event_callback(21, playcb)
GPIO.add_event_callback(13, nextcb)


# start player
print('loading ' + videoFile)
player = OMXPlayer(videoFile, args=['--loop'],
                   dbus_name='org.mpris.MediaPlayer2.omxplayer1')
# player = OMXPlayer(videoFile, dbus_name='org.mpris.MediaPlayer2.omxplayer1')
print(player.metadata())
#player.stopEvent += lambda _: nextcb(0)
#player.positionEvent += lambda _: nextcb(0)

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
        #print(player.position(), sep= ' ', end = ' ', flush = True)
        sleep(1)
        try:
            if player.can_control():
                if player.position() > durations[durationIndex]:
                    print('NEXT')
                    nextcb(0)
        except:
            print('goin on')
        # do nothing
        pass


# cleanup
except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    player.quit()
