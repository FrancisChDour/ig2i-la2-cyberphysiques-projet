#!/usr/bin/env python3
import serial
import time
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
    ser.flush()
    time.sleep(3)
    ser.write(b"200,200")
    time.sleep(3)
    ser.write(b"100,100")
