from picamera import PiCamera
from gpiozero import MotionSensor
from gpiozero import Button
from time import sleep
import os
import subprocess
import requests

# Some setup first:
USER_KEY = 'REPLACE_THIS_WITH_YOUR_USER_KEY'   # The user key for Pushover
API_TOKEN = 'REPLACE_THIS_WITH_YOUR_API_TOKEN'    # The app token for Pushover

print('Getting smart...')

# Set up all our devices
camera = PiCamera()
motion = MotionSensor(17)
doorSensor = Button(26)
letterbox = Button(19)
doorbell = Button(13)


# Send a pushover alert
def pushover(message, attachment=None):
    attachDict = {}
    if attachment is not None:
        attachDict['attachment'] = ("image.jpg",
                                    open(attachment, "rb"), "image/jpeg")

    print('Alerting: ' + message)
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": API_TOKEN,
        "user": USER_KEY,
        "title": "Smart door alert",
        "message": message
    },
        files=attachDict
    )


def motionDetected():
    print('Motion detected, video recording')
    os.system('DISPLAY=:0 xset s reset')  # Wakes the display up
    camera.start_preview()
    camera.start_recording('/home/pi/Desktop/motion.h264')
    pushover('Incoming!')
    sleep(10)


def motionStopped():
    print('Stopping video recording')
    camera.stop_recording()
    camera.stop_preview()


def doorOpen():
    pushover('Door open')


def doorClosed():
    pushover('Door closed')


def letterboxOpen():
    pushover('You got mail!')


def doorbellPressed():
    subprocess.Popen(['mpg123', '/home/pi/smartdoor/doorbell.mp3'],
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    camera.capture('/home/pi/Desktop/doorbell.jpg')
    pushover('Someone\'s at the door!', '/home/pi/Desktop/doorbell.jpg')

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
