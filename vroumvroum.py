#!/usr/bin/env python3

import serial

ser = None

def setup():
    global ser
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
    ser.flush()

def move(v1, v2):
    ser.write("{},{}".format(-v1,v2).encode('utf-8'))

left = 0
right = 0

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