#!/usr/bin/env python3

from marvelmind import MarvelmindHedge
from time import sleep
import sys
import serial
from math import cos, sin, acos, sqrt, degrees, pi

HEDGE_ID = 50

hedge = None
ser = None

def readGPS():
    position = hedge.position()
    while position[0] != HEDGE_ID:
        position = hedge.position()
    return position

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
    ser.write("{},{}".format(-v1,v2).encode('utf-8'))

left = 0
right = 0
setup()

def teta(xa, ya, xb, yb):
    x = xb - xa
    y = yb - ya
    return degrees(acos(y/sqrt(x**2+y**2)) - (pi/2))

while True:
    k = input()
    if(k == "z"):
        left+=50
        right+=50
        print(left, right)
        move(left, right)
    if(k == "s"):
        left-=50
        right-=50
        print(left, right)
        move(left, right)
    if(k == "q"):
        left-=50
        right+=50
        print(left, right)
        move(left, right)
    if(k == "d"):
        left+=50
        right-=50
        print(left, right)
        move(left, right)
    if(k == "a"):
        left=0
        right=0
        print(left, right)
        move(left, right)
    if(k == "e"):
        print(readGPS())