from picamera import PiCamera
from time import sleep

camera = PiCamera()

# camera lets you have 5 second to prepare and then takes a photo
camera.start_preview()

sleep(5)
camera.capture('/home/pi/Desktop/image.jpg')

camera.stop_preview()

# camera takes a video

sleep(3)
camera.start_preview()
camera.start_recording('/home/pi/Desktop/video.h264')
sleep(3)
camera.stop_recording()
camera.stop_preview()

