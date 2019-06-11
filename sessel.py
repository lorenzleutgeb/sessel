import functools
import gpiozero
import pygame
import sys
import time

from subprocess import call

# To install dependencies, run the following (tested on Raspbian):
# sudo apt-get install python-gpiozero python-pygame

# Pins to use. Read the gpiozero manual on how to specify pins, and
# consider that older models only offer a smaller number of pins, as
# can be seen on Wikipedia.
# WARNING: Choosing/wiring the wrong pins might damage your Raspberry Pi!
# https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering
# https://en.wikipedia.org/wiki/Raspberry_Pi#General_purpose_input-output_(GPIO)_connector
PINS = [
    "GPIO4" , # PIN7
    "GPIO18", # PIN12
    "GPIO27", # PIN13
    "GPIO24"  # PIN18
]

print "Setting volume to 100%"
call(["amixer", "-q", "sset", "'PCM'", "90%"])

if sys.argv[0] != __file__ or len(sys.argv) < 2:
    print "Run this file as follows:\n\tpython " + __file__ + " [list of sound files separated by space]"

args = sys.argv[1:]
print args
n = len(args)

if n > len(PINS):
    print "You requested to mix " + str(n) + " sound files, but only " + str(len(PINS)) + " pins are available."
    sys.exit(1)

print "Initializing pygame..."
pygame.init()
pygame.mixer.init(channels=n)

# Channels, Sounds and Buttons (one per sound file)
ch = [None] * n
so = [None] * n
bt = [None] * n

rewind_requested = False

print "PIN\tFILE"
for i in range(n):
    print str(PINS[i]) + "\t" + args[i]
    so[i] = pygame.mixer.Sound(args[i])

def rewind_if_requested():
    global rewind_requested
    if rewind_requested:
        rewind_requested = False
        rewind()

def rewind():
    print "Rewinding"
    for i in range(n):
        ch[i].stop()
        ch[i].play(so[i], loops=-1)
        ch[i].set_volume(0)

def request_rewind():
    global rewind_requested
    print "Rewind requested"
    rewind_requested = True

def pressed(i):
    rewind_if_requested()
    print str(i) + " pressed"
    ch[i].set_volume(1)

def released(i):
    print str(i) + " released"
    ch[i].set_volume(0)

rewind_button = gpiozero.Button("GPIO25") # PIN22
rewind_button.when_pressed = request_rewind

for i in range(n):
    bt[i] = gpiozero.Button(PINS[i])
    bt[i].when_pressed  = functools.partial(pressed, i)
    bt[i].when_released = functools.partial(released, i)

print "Sounds initialized."

for i in range(n):
    ch[i] = so[i].play(loops=-1)
    ch[i].set_volume(0)

print "---"

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print "Ciao!"
        sys.exit(0)
