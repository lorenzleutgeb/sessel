import functools
import gpiozero
import pygame
import sys
import time

# Pins to use. Read the gpiozero manual on how to specify pins, and
# consider that older models only offer a smaller number of pins, as
# can be seen on Wikipedia.
# WARNING: Choosing/wiring the wrong pins might damage your Raspberry Pi!
# https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering
# https://en.wikipedia.org/wiki/Raspberry_Pi#General_purpose_input-output_(GPIO)_connector
# TODO: Extend this to at least 8 pins.
PINS = [ 7, 14 ]

if sys.argv[0] != __file__ or len(sys.argv) < 2:
    print "Run this file as follows:\n\tpython " + __file__ + " [list of sound files]"

args = sys.argv[1:]
print args
n = len(args)

if n > len(PINS):
    print "You requested to mix " + str(n) + " sound files, but only " + str(len(PINS)) + " pins are available."
    sys.exit(1)

print "Initializing pygame..."
pygame.init()
pygame.mixer.init(channels=n)

# Channels and Buttons (one per sound file)
ch = [None] * n
bt = [None] * n

def pressed(i):
    print str(i) + " pressed"
    ch[i].set_volume(1)

def released(i):
    print str(i) + " released"
    ch[i].set_volume(0)

print "PIN\tFILE"
for i in range(n):
    print str(PINS[i]) + "\t" + args[i]
    ch[i] = pygame.mixer.Sound(args[i]).play(loops=-1)
    bt[i] = gpiozero.Button(PINS[i])
    ch[i].set_volume(0)

    bt[i].when_pressed  = functools.partial(pressed, i)
    bt[i].when_released = functools.partial(released, i)

print "---"

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print "Ciao!"
        sys.exit(0)
