#!/usr/bin/env python3
import serial
import time
import sys

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
    ser.flush()
    ser.write("0,0").encode('utf-8'))
