#!/usr/bin/python

import RPi.GPIO as GPIO
import time

#------------------
# Global Settings
#
# Debug flag
debug = 1

# GPIO mode
if debug: print "set mode to GPIO.BCM mode (GPIO 0 = GPIO 17 (BCM) = Pin 11 (phys.))"
GPIO.setmode(GPIO.BCM)

# Set GPIO02 to falling edge detection
GPIO.setup(02, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Double Click Settings
delta = 0.5                   # time in between interrupts to detect double click
token_double = 0

#------------------
# Callback Function
#
# Interrupter
#   React on pushing the button
def interrupter(channel):
    global unique_id
    try:
        unique_id
    except NameError:
        unique_id = -1
    unique_id = unique_id + 1
    print "unique_id = ", unique_id
    # Time button pressed
    # make time_last global and check if it already exists
    global time_last
    try:
        time_last
    except NameError:               # only execute first time
        time_last = time.time() - 10
    # look at current time
    time_start = time.time()
    
    # Token for ignoring single clicks when detecting double clicks
    global token_double
    try:
        token_double
    except NameError:               # set as 0 the first time
        token_double = 0
        
    if token_double == 0:
        token_double = 1
        time.sleep(2*delta)
        if token_double == 1:
            print "single!"
            token_double = 0
    else:
        token_double
        "double"
    #~ if (time_start-time_last) < delta:
        #~ print "Double click detected"
        #~ token_double = 1
    #~ else:
        #~ time_last = time.time()
        #~ while time.time()-time_start < delta:
            #~ time.sleep(0.1)
            #~ print token_double
        #~ if token_double == 0:
            #~ print "Single click detected"
        #~ token_double = 0
    #~ time_last = time.time()

# Event Detection
GPIO.add_event_detect(02, GPIO.FALLING, callback=interrupter, bouncetime=150)

#------------------
# Self-Test
#
# Only active if called directly as main
if __name__ == "__main__":
    print "Selftest!"
    while True:
        time.sleep(3)
        print "Nothing: token_double = ", token_double

