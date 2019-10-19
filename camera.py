#!/usr/bin/python3

from picamera import PiCamera

camera = PiCamera()
camera.resolution(512, 768)
camera.start_preview()

# Camera warm-up time
sleep(2)
camera.capture('pytest.jpg')
