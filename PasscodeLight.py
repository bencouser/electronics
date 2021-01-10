import RPi.GPIO as GPIO 
from time import sleep

PASSWORD = [0,1,1,8] 
guess = [] 
numberPresses = 0

GPIO.setmode(GPIO.BOARD)

MATRIX = [[1,2,3,'A'],
          [4,5,6,'B'],
          [7,8,9,'C'],
          ['*',0,'#','D']]

ROW = [7,11,13,15]
COL = [12,16,18,22]

REDPin = 36
GREENPin = 40
GPIO.setup(REDPin, GPIO.OUT)
GPIO.setup(GREENPin, GPIO.OUT)
blinkCount = 0

for j in range(4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 1)

for i in range(4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

try:
    print("Please enter the passcode")
    while(numberPresses < 4):
        for j in range(4):
            GPIO.output(COL[j],0)#low checkig input 

            for i in range(4):
                if GPIO.input(ROW[i]) == 0:
                    print MATRIX[i][j]
                    guess.append(MATRIX[i][j])
                    numberPresses += 1
                    while(GPIO.input(ROW[i]) == 0): # button hold downs
                        pass

            GPIO.output(COL[j],1)# high

    if guess == PASSWORD:
        print("Correct Password")
        while(blinkCount < 3):
            GPIO.output(GREENPin, True) 
            sleep(0.5) 
            GPIO.output(GREENPin, False)
            sleep(0.5)
            blinkCount += 1
            GPIO.setup(GREENPin, GPIO.OUT) 
    else:
        print("INCORRECT POSSWORD!")
        while(blinkCount < 3):
            GPIO.output(REDPin, True) 
            sleep(0.5) 
            GPIO.output(REDPin, False)
            sleep(0.5)
            blinkCount += 1
            GPIO.setup(REDPin, GPIO.OUT) 

except KeyboardInterrupt:
    GPIO.cleanup()

finally:
    GPIO.cleanup()
