#!/usr/bin/env python3

from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import sys
import RPi.GPIO as GPIO

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# gpio callbacks
def playcb(channel):
    print('play callback')

def nextcb(channel):
    print('next callback')

# gpio event setup
GPIO.add_event_detect(13, GPIO.RISING, bouncetime=200)
GPIO.add_event_detect(21, GPIO.RISING, bouncetime=200)
GPIO.add_event_callback(21, playcb)
GPIO.add_event_callback(13, nextcb)

arg = sys.argv[1]

#import logging
#logging.basicConfig(level=logging.INFO)


VIDEO_1_PATH = arg
#print(VIDEO_1_PATH)
#player_log = logging.getLogger("Player 1")

player = OMXPlayer(VIDEO_1_PATH, dbus_name='org.mpris.MediaPlayer2.omxplayer1')
#player.playEvent += lambda _: player_log.info("Play")
#player.pauseEvent += lambda _: player_log.info("Pause")
#player.stopEvent += lambda _: player_log.info("Stop")

# it takes about this long for omxplayer to warm up and start displaying a picture on a rpi3
sleep(2.5)

times=[]

for i in range(0,20):
    #sleep(2)
    player.set_position(0)
    player.pause()
    player.hide_video()

    #sleep(2)
    player.show_video()


    #player.set_aspect_mode('stretch')
    #player.set_video_pos(0, 0, 200, 200)
    player.play()

    sleep(20)

    times.append(float("{0:.3f}".format(player.position())))

player.quit()

diffs=[]

for i in range(len(times)-1):
    diff=float("{0:.3f}".format(times[i+1]-times[i]))
    diffs.append(abs(diff))

avgdiffs = sum(diffs)/float(len(diffs))

print("times:   " + str(times))
print("diffs:   " + str(diffs))
print("maxdiff: " + str(max(diffs)))
print("avgdiffs:" +str(avgdiffs))
