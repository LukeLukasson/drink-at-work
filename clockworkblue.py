#!/usr/bin/python

#------------------
# Milestones:
#
#	x	Count down and simulate LEDs
#   x   Simulate snooze button by pressing enter
#	x	Include smart cycles including working hours and amount of water
#   o   Constant amount of LEDs -> adapt interval accordingly
#   x   Mount LEDs (with Charlieplexing)
#   o   Easy Interface to start and stop and reset system
#   o   Settings externally available and dynamically changeable
#   o   Mute switch

#------------------
# Simplifications/Mitigations:
#
#   x   Interval fixed at 0.3 -> adapt interval with remaining time
#   o   Constant working hours (always 8h)
#   o   Ignore lunch time
#   o   What happens if you drink in between warnings?
#   o   Only considering mornings (to end at 11.30) -> ignoring afternoons (to end at 16.00)

import datetime
import time
import ledcontrol

#------------------
# Global Settings
#
# Debug flag
debug = 1                       # 0 false; 1 true

# Drinking Settings
l_tot = 1.4                     # total amount of water to drink per day
l_gone = 0                      # water drank till start of day
l_interval = 0.2                # goal to drink each t_def

# Timing Settings
t_tot = 4 * 60 * 4              # total of hours at desk in [s]
t_def = 50                      # default interval in [s]
t_ad = t_def                    # adapted interval in [s] (start the day with a glass of water -> t_ad = 0)

# LED Settings
n_leds = 12                     # number of LEDs available

# Counters
c_morning = 7



#------------------
# Help Functions
#
# Countdown
#   Input:      n   Number of seconds
def countdown(n):
	part = int(n/n_leds)
	if debug: print "time in s = " + str(n) + " and part = " + str(part)
	cntdwn_start = datetime.datetime.now()
	for i in range(n_leds,0,-1):			# i = 12 ... 1
		ledcontrol.light_level(i, part)
	return 0
    
# Light up LED
#   Input:      x       LED x
#   Output:     LED lights up
def led_shine(x):
    print x * "*"
    print "LED " + str(x) + " lights up!"
    return 0
    
# Time to drink!
def time_to_drink():
    print "-----"
    raw_input("Time to drink@work! Press ENTER to continue: ")
    #time.sleep(random.randint(0,5))
    print "Button pressed"
    return 0
    
# Update interval
#   Input:      n       Number of intervals left
#   Output:     t_ad    Time for next interval 
def update_interval(n):
    l_diff = l_tot - l_gone
    if debug: print "Still to drink: " + str(l_diff) + " [l]"
    t_diff = shift_end - datetime.datetime.now()
    if debug: print "Time left: " + str(t_diff)
    if n > 0:
        if debug: print "Number of cycles left: " + str(n) + "   -> " + str(t_diff/n) + " for next cycle"
        return t_diff/n     # divide time left by number of drinking cicles left
    else:
        return t_diff

#------------------
# Algorithm
shift_start = datetime.datetime.now()
if debug: print "Shift started: " + str(shift_start)
shift_end = shift_start + datetime.timedelta(hours=1)
if debug: print "Shift to end:  " + str(shift_end)

while l_gone < l_tot:
    if debug: print "t_ad = " + str(t_ad)
    countdown(t_ad)                 # start countdown
    time_to_drink()                 # countdown finished
    l_gone += l_interval            # amount of water drank
    c_morning -= 1                  # numbers of invervals left
    t_ad = update_interval(c_morning).seconds        # update remaining cycles
print "Enough for today: Good job!"

