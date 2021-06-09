#!/usr/bin/env python3

import keyboard
from marvelmind import MarvelmindHedge
from time import sleep
import sys
import serial

hedge = None
ser = None

left = 0
right = 0

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

while True:
    k = keyboard.read_key()
    if(k == "z"):
        left+=20
        right-=20
        move(left, right)
        print("pressed z")
    elif(k == "s"):
        left-=20
        right+=20
        move(left, right)
        print("pressed s")
    elif(k == "a"):
        left=0
        righ=0
        move(left, right)
        print("pressed a")