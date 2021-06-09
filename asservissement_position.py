*#!/usr/bin/env python3

from marvelmind import MarvelmindHedge
from time import sleep
import sys
import serial
from math import cos, sin, acos, sqrt, degrees
import re

HEDGE_ID = 50
GAIN_K = 0.66
WHEEL_RADIUS = 35
LONG = 100

hedge = None
ser = None
tetaC = None

def main():
	setup()
	calibrage()
	tourniquet(5,0)

def marchePo():
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
    hedge = setup()
    ser.flush()
    while True:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                if(len(line) < 21):
                    print(len(line))
                    continue
                print(line)
                angle = line.split(' ')[2][2::]
                position = readGPS(hedge)
                result = position[1:4] + [angle]
                print('X:{} Y:{} Z:{} θ:{}'.format(result[0], result[1], result[2], result[3]))
                tension_x, tension_y = correction(5,0, float(result[0]), float(result[1]))
                linear_speed, lrotation_speed = rotation_matrix(tension_x, tension_y, float(result[3]))
                v1, v2 = commande(linear_speed, lrotation_speed/LONG)
                v1*=100
                v2*=100
                print("v1:{},v2:{}".format(v1,v2))
                ser.write("{},{}".format(v1, v2).encode('utf-8'))
                sleep(0.001)
        except KeyboardInterrupt:
            hedge.stop()  # stop and close serial port
            ser.write("0,0".encode('utf-8'))
            sys.exit()

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


def commande(lineare_speed, rotation_speed):
    v1 = lineare_speed + rotation_speed * WHEEL_RADIUS
    v2 = lineare_speed - rotation_speed * WHEEL_RADIUS
    return v1, v2

def rotation_matrix(tension_x, tension_y, teta):
    lineare_speed = tension_x * cos(teta) + tension_y * sin(teta)
    lrotation_speed = -tension_y * sin(teta) + tension_y * cos(teta)
    return lineare_speed, lrotation_speed
   
def correction(position_x, position_y, return_position_x, return_position_y):
    ux = GAIN_K * (position_x - return_position_x)
    uy = GAIN_K * (position_y - return_position_y)
    return ux, uy

def teta(xa, ya, xb, yb):
    x = xb - xa
    y = yb - ya
    return degrees(acos(x/sqrt(x**2+y**2)))

def calibrage():
    sleep(2)
    firstPosition = readGPS()
    moove(-200,200)
    sleep(5)
    ser.write("0,0".encode('utf-8'))
    sleep(2)
    lastPosition = readGPS()
    print(firstPosition)
    print(lastPosition)
    t = teta(firstPosition[1], firstPosition[2], lastPosition[1], lastPosition[2])
    print(t)
    global tetaC = t

def tourniquet(x, y):
	firstP = readGPS()
	to = teta(firstP[1], firstP[2], x, y)
	print(t)
	tf = to - tetaC
	print("tf:{}".format(tf))
	
def moove(v1,v2):
	ser.write("{},{}".format(v1,v2).encode('utf-8'))

main()
