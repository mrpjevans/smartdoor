#
# Smart Porch Light
# PJ Evans @mrpjevans
#
from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.util import load_json, save_json
from time import sleep
import json
from gpiozero import MotionSensor
import requests
import arrow

# Chnage these setting as needed
MY_LAT = "LATITUDE"
MY_LONG = "LONGITUDE"
LIGHT_OFF_MANUAL = '00:00'  # Overides sunrise
GATEWAY_IP_ADDRESS = 'IP_ADDRESS_OF_TRADFRI_GATEWAY'
CONFIG_FILE = '/home/pi/smartdoor/tradfri_standalone_psk.conf'
SUN_RISE_SET_DOWN_API = 'https://api.sunrise-sunset.org/json?lat=' + MY_LAT + '&lng=' + MY_LONG + '&formatted=0'

# PIR Detector
motion = MotionSensor(17)

# Default brightness state (off)
brightness = 0
newBrightness = 0

# Sun rise/set info
sunTimes = {}
sunrise = 0
sunset = 0
ticktock = 300

# Load in the config file, get our password for the gateway and create an API
conf = load_json(CONFIG_FILE)
identity = conf[GATEWAY_IP_ADDRESS].get('identity')
psk = conf[GATEWAY_IP_ADDRESS].get('key')
api_factory = APIFactory(host=GATEWAY_IP_ADDRESS, psk_id=identity, psk=psk)

# This section connects to the gateway and gets information on devices
api = api_factory.request
gateway = Gateway()
devices_command = gateway.get_devices()
devices_commands = api(devices_command)
devices = api(devices_commands)

# Create an array of objects that are lights. Our porch light is 0.
lights = [dev for dev in devices if dev.has_light_control]
porchLight = lights[0]

# Start with the light off
api(porchLight.light_control.set_dimmer(brightness))

while True:

    # Motion detection
    inMotion = False
    if motion.motion_detected:
        print('Motion detected, setting light to 254')
        api(porchLight.light_control.set_dimmer(254))
        inMotion = True

    while inMotion and motion.motion_detected:
        sleep(10)

    if inMotion:
        print('Setting light to ' + str(brightness))
        api(porchLight.light_control.set_dimmer(brightness))

    # Only do this once a minute
    if ticktock == 300:

        ticktock = 0
        print('Checking times')

        # If we have data, is it still for today?
        if sunrise == 0 or arrow.get(sunrise).to('local').format('YYYY-MM-DD') != arrow.now().format('YYYY-MM-DD'):
            print('Date has changed, or first run. Refreshing information')
            r = requests.get(SUN_RISE_SET_DOWN_API)
            sunTimes = r.json()
            sunrise = int(arrow.get(sunTimes['results']['sunrise']).to('local').format('X'))
            sunset = int(arrow.get(sunTimes['results']['sunset']).to('local').format('X'))
            print('Today the sun will rise at ' + arrow.get(sunrise).format('HH:mm') + ' and set at ' + arrow.get(sunset).format('HH:mm'))

            # If manual off set, override
            if LIGHT_OFF_MANUAL is not None:
                sunrise = int(arrow.get(arrow.now().format('YYYY-MM-DD') + ' ' + LIGHT_OFF_MANUAL + ':00').format('X'))
                print('Light off time overridden to ' + LIGHT_OFF_MANUAL)

        # Current time
        now = int(arrow.now().format('X'))

        # Is before today's sunrise and the light is off?
        if now < sunrise and brightness == 0:
            newBrightness = 50

        # Is after today's sunrise, before sunset and the light is on?
        if now >= sunrise and now < sunset and brightness != 0:
            newBrightness = 0

        # Is after today's sunset and the light is off?
        if now >= sunset and brightness == 0:
            newBrightness = 50

        # Is before today's sunset and the light is on?
        if now < sunset and brightness != 0:
            newBrightness = 0

        # Set light if changed
        if brightness != newBrightness:
            print('Setting light to ' + str(newBrightness))
            api(porchLight.light_control.set_dimmer(newBrightness))
            brightness = newBrightness

    sleep(0.2)
    ticktock += 1
