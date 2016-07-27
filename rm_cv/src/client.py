#!/usr/bin/env python

import time
import random

while True:
    print "---"
    print random.choice(["blue", "red"])
    print float(random.randint(-1000,1000)) / 100
    print float(random.randint(-1000,1000)) / 100
    print float(random.randint(-1000,1000)) / 100
    time.sleep(0.04167)
