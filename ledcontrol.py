#!/usr/bin/python

#------------------
# Simplifications/Mitigations:
#
#   x   light_level: lights level while True -> does it stop when new light_level is called? -> token necessary?
#   o   maybe led_pause cannot be constant (trial and error)
#	o	introduce self testing function
#   o   Level 1 must blink!!! (or level below 1...)

# Use RPi.GPIO in order to control the GPIOs of the RaspberryPi 2
import RPi.GPIO as GPIO
import time
import datetime

#------------------
# Global Settings
#
# Debug flag
debug = 1

# Haptic limit
led_pause = 0.001            # 1 kHz -> short pause in between different LEDs will trick human eye
                                #   400 Hz > 11 * 30 Hz (maximal pause until same LED is light again)

# GPIO mode
if debug: print "set mode to GPIO.BCM mode (GPIO 0 = GPIO 17 (BCM) = Pin 11 (phys.))"
GPIO.setmode(GPIO.BCM)

# GPIOs
pins = [17, 18, 27, 22] # BCM

# 1 High, 0 Low, -1 HighImpedance
# defined by drawing
pin_led_states = [
  [1, -1, 0, -1], # 11
  [1, -1, -1, 0], # 10
  [0, -1, 1, -1], # 9
  [0, -1, -1, 1], # 8
  [-1, 0, 1, -1], # 7
  [-1, 1, -1, 0], # 6
  [-1, 1, 0, -1], # 5
  [-1, 0, -1, 1], # 4
  [1, 0, -1, -1], # 3
  [-1, -1, 1, 0], # 2 (green)
  [0, 1, -1, -1], # 1 (orange)
  [-1, -1, 0, 1]  # 0 (red)
]

#------------------
# Help Functions
#
# Set single pin to state
#   Input:  pin_index       0, 1, 2, 3
#           pin_state       1 High, 0 Low, -1 HighImpedance
def set_pin(pin_index, pin_state):
    if pin_state == -1:           
        print pin_index
        print pins[pin_index]
        GPIO.setup(pins[pin_index], GPIO.IN)
        print "I got past the setup!"
    else:
        GPIO.setup(pins[pin_index], GPIO.OUT)
        if pin_state == 1:
            GPIO.output(pins[pin_index], GPIO.HIGH)
        if pin_state == 0:
            GPIO.output(pins[pin_index], GPIO.LOW)
        else:
            print "No valid input for pin_state: 1 High, 0 Low, -1 HighImpedance"

# Light up LED
#   Input:      led_number  Number of LEDs = Rows of matrix pin_led_states
def light_led(led_number):
    for pin_index, pin_state in enumerate(pin_led_states[11-led_number]):
        set_pin(pin_index, pin_state)
        
# Light up Level
#   Input:      level       Light up level 1 - 12
#				t			Time in [s]
def light_level(level, t):
	clear_pins()
	t_start = datetime.datetime.now()
	t_diff = datetime.datetime.now() - t_start
	while t_diff < datetime.timedelta(seconds=t):
		for n in range(0,level):         # go through all LEDs
			light_led(n)
			time.sleep(led_pause)
		t_diff = datetime.datetime.now() - t_start


# Clear Pins
def clear_pins():
	print "Set 0 to input"
	set_pin(0, -1)
	print "Set 1 to input"
	set_pin(1, -1)
	set_pin(2, -1)
	set_pin(3, -1)
        

#------------------
# Algorithm
if debug: print "set all pins to input"             # clear all pins
clear_pins()
while True:
	x = int(raw_input("Light up LED: "))
	light_led(x)
	time.sleep(2)
