#!/usr/bin/python

#------------------
# Simplifications/Mitigations:
#
#   o   light_level: lights level while True -> does it stop when new light_level is called? -> token necessary?
#   o   maybe led_pause cannot be constant (trial and error)

# Use wiringpi2 in order to control the GPIOs of the RaspberryPi 2
import wiringpi2 as wiringpi
import time

#------------------
# Global Settings
#
# Debug flag
debug = 1

# Haptic limit
led_pause = 0.0025            # 400 Hz -> short pause in between different LEDs will trick human eye
                                #   400 Hz > 11 * 30 Hz (maximal pause until same LED is light again)

# GPIO mode
if debug: print "set mode to wiringpi mode (GPIO 0 = GPIO 17 (BCM) = Pin 11 (phys.))"
wiringpi.wiringPiSetup()

# GPIOs
pins = [0, 1, 2, 3]

# 1 High, 0 Low, -1 HighImpedance
# defined by drawing
pin_led_states = [
  [1, -1, 0, -1], # 11
  [1, -1, -1, 0], # 10
  [0, -1, 1, -1], # 9
  [0, -1, 1, -1], # 8
  [-1, 0, 1, -1], # 7
  [-1, 1, -1, 0], # 6
  [-1, 1, 0, -1], # 5
  [-1, 0, -1, 1], # 4
  [1, 0, -1, -1], # 3
  [-1, -1, 1, 0], # 2
  [0, 1, -1, -1], # 1
  [-1, -1, 0, 1]  # 0
]

#------------------
# Help Functions
#
# Set single pin to state
#   Input:  pin_index       doesn't matter which GPIO mode
#           pin_state       0 input, 1 output, 2 alternative function
def set_pin(pin_index, pin_state):
    if pin_state == -1:
	    if debug: print "set pin " + str(pin_index) + " (" + str(pins[pin_index]) + ") to input"
        wiringpi.pinMode(pins[pin_index], 0)
    else:
	    if debug: print "set pin " + str(pin_index) + " (" + str(pins[pin_index]) + ") to output"
        wiringpi.pinMode(pins[pin_index], 1)
        wiringpi.digitalWrite(pins[pin_index], pin_state)

# Light up LED
#   Input:      led_number  Number of LEDs = Rows of matrix pin_led_states
def light_led(led_number):
    for pin_index, pin_state in enumerate(pin_led_states[led_number]):
        set_pin(pin_index, pin_state)
        
# Light up Level
#   Input:      level       Light up level 1 - 12
def light_level(level):
    set_pin(0, -1)          # clear all pins
    set_pin(1, -1)
    set_pin(2, -1)
    set_pin(3, -1)
    while True:
        for n in range(0,level):         # go through all LEDs
            light_led(n)
            time.sleep(led_pause)
        

        

#------------------
# Algorithm
if debug: print "set all pins to input"             # clear all pins
set_pin(0, -1)
set_pin(1, -1)
set_pin(2, -1)
set_pin(3, -1)

if debug: print "start while loop"
while True:
    x = int(raw_input("Level (1 to 12):"))
    light_level(x)
