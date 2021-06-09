#!/usr/bin/env python3

from marvelmind import MarvelmindHedge
from time import sleep
import sys
import serial
from math import cos, sin, acos, sqrt, degrees
import re
import keyboard

hedge = None
ser = None
tetaC = None

angle_resultat = None

def main():
    setup()
    left = 0
    right = 0
    while True:
        if keyboard.read_key() == "z":
            print("You pressed z")
            left+=25
            right+=25
        if keyboard.read_key() == "s":
            print("You pressed s")
            left-=25
            right-=25
        if keyboard.read_key() == "d":
            print("You pressed s")
            left+=25
            right-=25
        if keyboard.read_key() == "q":
            print("You pressed q")
            left-=25
            right+=25
        if keyboard.read_key() == "a":
            print("You pressed q")
            left=0
            right=0
        move(left, right)

def setup():
    global hedge
    global ser
    hedge = MarvelmindHedge(tty="/dev/ttyACM0", adr=None, debug=False)  # create MarvelmindHedge thread
    if (len(sys.argv) > 1):
        hedge.tty = sys.argv[1]
    hedge.start()
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
    ser.flush()

def move(v1, v2):
    ser.write("{},{}".format(v1,v2).encode('utf-8'))

main()
