#!/usr/bin/python

#------------------
# Simplifications/Mitigations:
#
#   o   light_level: lights level while True -> does it stop when new light_level is called? -> token necessary?
#   o   maybe led_pause cannot be constant (trial and error)

# Use wiringpi2 in order to control the GPIOs of the RaspberryPi 2
import wiringpi2 as wiringpi
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
#   Input:  pin_index       doesn't matter which GPIO mode
#           pin_state       0 input, 1 output, 2 alternative function
def set_pin(pin_index, pin_state):
    if pin_state == -1:           
        wiringpi.pinMode(pins[pin_index], 0)
    else:
        wiringpi.pinMode(pins[pin_index], 1)
        wiringpi.digitalWrite(pins[pin_index], pin_state)

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
    set_pin(0, -1)
    set_pin(1, -1)
    set_pin(2, -1)
    set_pin(3, -1)
        

#------------------
# Algorithm
if debug: print "set all pins to input"             # clear all pins
clear_pins()

if debug: print "start while loop"
while True:
    x = int(raw_input("Light up LED: "))
    light_led(x)
    time.sleep(2)
    light_level(12, 2)
    for i in range(1,13):
		if debug: print "Level = " + str(i)
		light_level(i, 0.5)
    clear_pins()
