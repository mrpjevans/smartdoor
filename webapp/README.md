# Smart Door Webapp

This is the 'advanced' webapp to accompany the tutorial in MagPi #77. It's not 'complete' but
where would be the fun in that?

## Features

Intended as a mobile-first webapp, this is simple control centre for the smartdoor project.

- Static photo of the doorcam
- Streaming video from the doorcam
- Log of door 'activity' (unimplemented)
- Log of letterbox 'activity' (unimplemented)
- Log of all activity (unimplemented)
- Unlock the door

## Hardware Requirements

- Pimoroni Automation HAT for door lock control
- Official camera module

## Physical

If you are using a magentic door lock, wire it to Relay 1 on the Automation HAT using NC (Normally Closed).

## Installation

This assumes the hostname of the server is 'smartdoor', so 'smartdoor.local' resolves.

Start with a Raspberry Pi OS Buster Lite installation. Make sure you have a network connection, SSH enabled and
have set the hostname (smartdoor) and changed the password.

```
sudo apt -y update && sudo apt -y upgrade
sudo apt install python3-flask git cmake libjpeg8-dev
curl https://get.pimoroni.com/automationhat | bash
git clone https://github.com/jacksonliam/mjpg-streamer.git
cd mjpg-streamer/mjpg-streamer-experimental
make
sudo make install
git clone https://github.com/mrpjevans/smartdoor.git
```

## Running

Both the video streamer and the smartdoor app need to be running.

Manualy:

```
cd ~/mjpg-streamer/mjpg-streamer-experimental
export LD_LIBRARY_PATH=.
./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so" &
cd ~/smartdoor/webapp
FLASK_APP=smartdoor.py FLASK_ENV=development flask run --host 0.0.0.0 &
```

You can now access the app:

```
http://smartdoor.local:5000/
```

## Disclaimer

This is a 'skeleton' app. It's a starting point for you to build something amazing. Logging needs to be implemented
and you may wish to change behaviour of certain things. Fork it, play around, have fun. I'll try and answer any
questions you have.

Finally, THIS IS JUST FOR FUN. It is not intended to be a secure or tested solution of any kind. There is no guarantee
or warranty implied.
