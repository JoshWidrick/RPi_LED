RPi LED
======

Overview
---
This is a simple system to control programmable LED strip(s) with a Raspberry Pi. 
The system includes a Flask app for user control.


Hardware
---
#### Required Hardware:
```
- Raspberry Pi (Im using a Pi 4 Model B)
- WS2812B LED Strip(s)
- 5v PSU (~5amp/strip in my case)
- Wires to connect it all together
```

#### PI 4 Model B GPIO Pin Layout:
![Pi and GPIO Pins](images/pi_and_gpio_pins.png)

#### Connecting Power:
The PSU should be plugged directly into the positive and negative ends of the LED strips.
Ground should also go from each strip into the Pi itself through any ground pin. Finally the Pi
should be powered through its usual power port (USB-C for Pi 4 Model B).

#### Connecting Strips to Pi:
The connection from the stips to the Pi is simple. You must use a GPIO port that supports PMW. In my case, 
I have two strips, so I used the GPIO12 and GPIO18 pins for the data connection. This is reflected in 
src/config.py. If you set your data ports up differently for some reason, or only have one strip, you 
will have to update src/config.py and possibly the strip formation in src/ledcontroller.py.


Installation
---
/home/pi/leds copy in /src for all controllers, and /web into the first. 


Usage
---
Must run both webapp.py and ledcontroller.py as superuser in separate console windows. 
Something such as TMUX helps alot. 


Modes
---
#### Block:
Instantly sets the strip to the chosen color(s).

#### Wipe:
Sets the strip to the chosen color(s) by wiping the state.

#### Starlight:
Sets individual LEDs to 'twinkle' like a star (dim on and dim off).

#### Chase:
Sets individual or blocks of LEDs to 'chase' through the strip.

#### Rave:

#### Wave:

#### Breathing:

#### Rainbow:
All the other modes allow for rainbow color settings, but this is something special (it's just a rainbow
wave, but still here cause it inspired a lot).
