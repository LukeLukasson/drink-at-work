import RPi.GPIO as GPIO

# GPIOs
pins = [17, 18, 27, 22]

# 1 High, 0 Low, -1 HighImpedance
pin_led_states = [
  [1, -1, 0, -1], # 12
  [1, -1, -1, 0], # 11
  [0, -1, 1, -1], # 10
  [0, -1, 1, -1], # 9
  [-1, 0, 1, -1], # 8
  [-1, 1, -1, 0], # 7
  [-1, 1, 0, -1], # 6
  [-1, 0, -1, 1], # 5
  [1, 0, -1, -1], # 4
  [-1, -1, 1, 0], # 3
  [0, 1, -1, -1], # 2
  [-1, -1, 0, 1]  # 1
]

print "set mode to GPIO.BCM"
GPIO.setmode(GPIO.BCM)

def set_pin(pin_index, pin_state):
    if pin_state == -1:
	print "set pin " + str(pin_index) + " (" + str(pins[pin_index]) + ") to input"
        GPIO.setup(pins[pin_index], GPIO.IN)
	print "success"
    else:
        GPIO.setup(pins[pin_index], GPIO.OUT)
        GPIO.output(pins[pin_index], pin_state)

def light_led(led_number):
    for pin_index, pin_state in enumerate(pin_led_states[led_number]):
        set_pin(pin_index, pin_state)

print "set all pins to input"
set_pin(0, -1)
set_pin(1, -1)
set_pin(2, -1)
set_pin(3, -1)

print "start while loop"
while True:
    x = int(raw_input("Pin (0 to 11):"))
    light_led(x)
