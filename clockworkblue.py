#!/usr/bin/python
#
# Milestones:
#
#	x	Count down and simulate LEDs
#	o	Include smart cycles including working hours and amount of water

import time


print "Starting Countdown"



# Countdown
#   Input:      n   Number of seconds
def countdown(n):
    while n > 0:
        print (n)
        led_shine(n)
        n -= 1
        time.sleep(1)
    print "countdown done"
    
# Light up LED
#   Input:      x   LED x
#   Output:     LED lights up
def led_shine(x):
    print "LED " + str(x) + " lights up!"

countdown(5)
