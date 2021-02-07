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
from picamera import PiCamera
import time
import datetime

camera = PiCamera()

GPIO.setmode(GPIO.BOARD)
guesses = 0
opened = 0

# Key Code setup
PASSWORD = [4, 7, 8, 2]

MATRIX = [[1, 2, 3, 'A'],
          [4, 5, 6, 'B'],
          [7, 8, 9, 'C'],
          ['*', 0, '#', 'D']]

ROW = [7, 11, 13, 15]
COL = [12, 16, 18, 22]

for j in range(4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 1)
    GPIO.setup(ROW[j], GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Servo setup
GPIO.setup(32, GPIO.OUT)

p = GPIO.PWM(32, 50)
p.start(7.5)

try:
    while(guesses < 4):
        guesses += 1
        print("What is the index of the first term in the Fibonacci sequence to contain 1000 digits?")
        numberPresses = 0
        guess = []
        while(numberPresses < 4):
            for j in range(4):
                GPIO.output(COL[j], 0)

                for i in range(4):
                    if GPIO.input(ROW[i]) == 0:
                        print MATRIX[i][j]
                        guess.append(MATRIX[i][j])
                        numberPresses += 1
                        while(GPIO.input(ROW[i]) == 0):
                            pass

                GPIO.output(COL[j], 1)

        if guess == PASSWORD:
            print("CORRECT ANSWER")
            p.ChangeDutyCycle(12.50) # box is unlocked in this state
            print("Box unlocked, press * to lock.")
            opened = True
            GPIO.output(COL[0], 0)
            while(opened):
                if GPIO.input(ROW[3]) == 0:
                    opened = False
            p.ChangeDutyCycle(7.50)
            print("Box is Locked.")
            guesses = 0
        else:
            print("INCORRECT ANSWER!")
            dt = str(datetime.datetime.now())
            camera.capture('/home/pi/Pictures/breakins/{}.jpg'.format(dt))

except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
    print("GPIO's are clean")

finally:
    p.stop()
    GPIO.cleanup()
    print("GPIO's are clean")
