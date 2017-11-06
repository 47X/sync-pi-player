#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time as time

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


#main
try:
    while True:
        #do nothing
        time.sleep(1)
        print('doin nothin')


#cleanup
except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit

GPIO.cleanup()           # clean up GPIO on normal exit








#!/usr/bin/env python3
#
# # gpio 21 and 13 btn to gnd when closed
#
# import RPi.GPIO as GPIO
# import time
#
# GPIO.setmode(GPIO.BCM)
#
# GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#
#
# while True:
#     playbtn = not GPIO.input(21)
#     nextbtn = not GPIO.input(13)
#     if playbtn:
#         print('Play Pressed')
#         time.sleep(0.002)
#     if nextbtn:
#         print('Next Pressed')
#         time.sleep(0.002)
