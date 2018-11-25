from picamera import PiCamera
from gpiozero import MotionSensor
from gpiozero import Button
from time import sleep
import os
import subprocess
import sys

print('Getting smart...')

# Set up all our devices
camera = PiCamera()
motion = MotionSensor(17)
doorSensor = Button(26)
letterbox = Button(19)
doorbell = Button(13)


def motionDetected():
    print('Motion detected, video recording')
    os.system('DISPLAY=:0 xset s reset')  # Wakes the display up
    camera.start_preview()
    camera.start_recording('/home/pi/Desktop/motion.h264')
    sleep(10)


def motionStopped():
    print('Stopping video recording')
    camera.stop_recording()
    camera.stop_preview()


def doorOpen():
    print('Door open')


def doorClosed():
    print('Door closed')


def letterboxOpen():
    print('You got mail!')


def doorbellPressed():
    subprocess.Popen(['mpg123', '/home/pi/smartdoor/doorbell.mp3'],
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    camera.capture('/home/pi/Desktop/doorbell.jpg')
    print('Someone\'s at the door!')

# Attach our functions to GPIOZero events
motion.when_motion = motionDetected
motion.when_no_motion = motionStopped
doorSensor.when_pressed = doorClosed
doorSensor.when_released = doorOpen
letterbox.when_released = letterboxOpen
doorbell.when_released = doorbellPressed

print('Smart door is smart')

# Loop forever allowing events to do their thing
try:
    while True:
        pass
except KeyboardInterrupt:
    print('Smart door no longer smart')
except:
    print('Oh dear')
