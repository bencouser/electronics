# I want to make a safe box that firstly requires a key card to be present
# and scanned to then let you type a pin number in (project euler questions
# answer) which will then cause a servo (that acts as a lock) to twist. Once
# closed we need to make it so that we can re-lock the box.

# I may need to have another acting lock as the servo may not be strong enough

# Some special cases: 
# card shown but pin never entered
# incorrect pin typed too many times
# power outage (we do not want the box to be unlocked without power present
# 

import RPi.GPIO as GPIO
import time

