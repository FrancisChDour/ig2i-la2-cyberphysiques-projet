#!/usr/bin/env python3

from marvelmind import MarvelmindHedge
from time import sleep
import sys
import serial

def main():
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
    ser.flush()
    hedge = setup()
    while True:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                angle = line.split(' ')[0][2::]
                result = readGPS(hedge)[1:4] + [angle]
                print('X:' + result[0] + ' Y:' + result[1] + ' Z:' + result[2] + ' θ:' + result[3])
        except KeyboardInterrupt:
            hedge.stop()  # stop and close serial port
            sys.exit()

def readGPS(hedge):
    return hedge.position()


def setup():
    hedge = MarvelmindHedge(tty="/dev/ttyACM0", adr=None, debug=False)  # create MarvelmindHedge thread
    if (len(sys.argv) > 1):
        hedge.tty = sys.argv[1]
    hedge.start()
    return hedge

main()
