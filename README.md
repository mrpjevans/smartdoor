# smartdoor
Code to accompany the smart door tutorial in MagPi #76

### Looking for the Webapp?

The 'webapp' folder referenced in the article will be appearing here very soon. Thank you for your patience.

### How To Start on Boot

A quick and easy way to start a Python script on boot is to add it to rc.local.

```
$ sudo nano /etc/rc.local 
```

Now find the last line, exit(0) and add something like this above it:

```
/usr/bin/python3 /home/pi/smartdoor.py &
```

Now the smartdoor monitor will run in the background as soon as the machine has started up. As this runs as root, remember re-install any dependancies installed with 'pip' using 'sudo pip'.
