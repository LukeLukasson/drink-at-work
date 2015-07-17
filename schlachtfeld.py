#!/usr/bin/python

import random
import time
import datetime

x = random.randint(0,30)

shift_start = datetime.datetime.now()
print shift_start
shift_end = datetime.datetime.combine(datetime.date.today(), datetime.time(11, 30, 00))
print shift_end

delta = shift_end - shift_start
print type(delta)
print delta

print delta / 6

print delta.seconds