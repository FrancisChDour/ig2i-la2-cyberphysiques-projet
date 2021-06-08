#!/usr/bin/env python3

from marvelmind import MarvelmindHedge
from time import sleep
import sys
import serial

HEDGE_ID = 50

def main():
    hedge = setup()
    while True:
        sleep(1)
        print(readGPS(hedge))

def readGPS(hedge):
    return hedge.position()


def setup():
    hedge = MarvelmindHedge(tty="/dev/ttyACM0", adr=None, debug=False)  # create MarvelmindHedge thread
    if (len(sys.argv) > 1):
        hedge.tty = sys.argv[1]
    hedge.start()
    return hedge

main()
