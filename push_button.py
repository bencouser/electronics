# In this program i have a led that is controled by a button thta can be turned on and off an arbitrary 3 times
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

blinkCount = 3
count = 0
LEDPin = 22
BUTTONPin = 5

# Setup the pin the LED is connected to
GPIO.setup(LEDPin, GPIO.OUT)

# Setup the button
GPIO.setup(BUTTONPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

BUTTONPress = True
LEDState = False

try:
    print("You can turn the light on and off 3 times.")
    while count < blinkCount:
        print("Come on and press the button!")
        BUTTONPress = GPIO.input(BUTTONPin)
        if BUTTONPress == False and LEDState == False:
            GPIO.output(LEDPin, True)
            print("LED ON")
            LEDState = True
            sleep(0.5)
        elif BUTTONPress == False and LEDState == True:
            GPIO.output(LEDPin, False)
            print("LED OFF")
            LEDState = False
            count += 1
            sleep(0.5)
        sleep(0.1)
    print("That's your 3 up buddy!")

finally:
    # Reset the GPIO pins to a safe state
    GPIO.output(LEDPin, False)
    GPIO.cleanup()

