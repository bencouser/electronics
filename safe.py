# I want to make a safe box that firstly requires a key card to be present
# and scanned to then let you type a pin number in (project euler questions
# answer) which will then cause a servo (that acts as a lock) to twist. Once
# closed we need to make it so that we can re-lock the box.

# I may need to have another acting lock as the servo may not be strong enough

# Some special cases: 
# card shown but pin never entered
# incorrect pin typed too many times
# power outage (we do not want the box to be unlocked without power present

# I Have realised the servo will not work with the lock i have printed
# will instead use a step motor

import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import datetime

camera = PiCamera()

GPIO.setmode(GPIO.BOARD)
guesses = 0
opened = 0

### Key Code setup ###

def nextTerm(a, b):
    return a + b

fibonacciNumbers = [1, 1]

def listFibNums(fibNums, N):
    for i in range(N):
        newTerm = newTerm(fibNums[i], fibNums[i + 1])
        if len(str(abs(newTerm))) == 1000:
            return i + 3
        fibNums.append(newTerm)

password = listFibNums(fibonacciNumbers, 100000)

PASSWORD = [int(x) for x in str(password)] #done so it aint as easy to steal code

### Key Pad Setup ###

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

### Step Motor Setup ###

# Config sp pins

ControlPins = [31, 33, 35, 37]

for pin in ControlPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Make Ctrln array for 8 set sequence for half stepping

seq = [[1, 0, 0, 0],
             [1, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 1],
             [0, 0, 0, 1],
             [1, 0, 0, 1]]

### Main Code ###

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
            for i in range(1000):
                for halfstep in range(8):
                    for pin in range(4):
                        GPIO.output(ControlPins[pin], seq[halfstep][pin])# box is unlocked in this state
                    time.sleep(0.001)
            print("Box unlocked, press * to lock.")
            opened = True
            GPIO.output(COL[0], 0)
            while(opened):
                if GPIO.input(ROW[3]) == 0:
                    opened = False
            for i in range(1000):
                for halfstep in range(8):
                    for pin in range(4):
                        GPIO.output(ControlPins[pin], seq[7 - halfstep][pin])# box is locked in this state
                    time.sleep(0.001)
            print("Box is Locked.")
            guesses = 0
        else:
            print("INCORRECT ANSWER!")
            dt = str(datetime.datetime.now())
            camera.capture('/home/pi/Pictures/breakins/{}.jpg'.format(dt))

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nGPIO's are clean")
