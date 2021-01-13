import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

# time module to add delay between turning on and off control pins

ControlPins = [7, 11, 13, 15]

for pin in ControlPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Make an array for 8 set sequence for half stepping

half_step = [[1, 0, 0, 0],
             [1, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 1],
             [0, 0, 0, 1],
             [1, 0, 0, 1]]
try:
    # cycle through the step array once
    for i in range(512):
        for step in range(8):
            for pin in range(4):
                GPIO.output(ControlPins[pin], half_step[step][pin])
            sleep(0.001) # time is to let the coils react (too quick to move 
                         # without the delay)
except KeyboardInterrupt:
    GPIO.cleanup()

finally:
    GPIO.cleanup()
