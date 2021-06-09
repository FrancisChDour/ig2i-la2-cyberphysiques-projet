#!/usr/bin/env python3

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

angle_resultat = None

def main():
    print("Setup")
    setup()
    print("Calibrage")
    calibrage()
    sleep(1)
    print("Tourniquet")
    tourniquet(5, 0)
    # print("Droit au but")
    # droitAuBut(5,0)
    # move(-250, 250)
    # for i in range (20):
    #     position = readGPS()
    #     result = position[1:4]
    #     print('X:{} Y:{} Z:{}'.format(result[0], result[1], result[2]))
    #     sleep(0.5)
    # move(0, 0)

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
    global tetaC
    sleep(2)
    first_position = readGPS()
    move(200, 200)
    sleep(5)
    move(0, 0)
    sleep(2)
    last_position = readGPS()
    print("firstPosition : ", first_position)
    print("lastPosition : ", last_position)
    t = teta(first_position[1], first_position[2], last_position[1], last_position[2])
    print("Teta : ", t)
    tetaC = t

def tourniquet(x, y):
    global angle_resultat
    first_position = readGPS()
    to = teta(first_position[1], first_position[2], x, y)
    angle_resultat = to - tetaC
    gyro_response = ser.readline().decode('utf-8').rstrip()
    while len(gyro_response) < 21:
        gyro_response = ser.readline().decode('utf-8').rstrip()
    print(gyro_response)
    angle_gyro = float(gyro_response.split(' ')[2][2::])
    move(50, -50)
    while angle_gyro < angle_resultat - 1 or angle_gyro > angle_resultat + 1:
        gyro_response = ser.readline().decode('utf-8').rstrip()
        while len(gyro_response) < 21:
            gyro_response = ser.readline().decode('utf-8').rstrip()
        angle_gyro = float(gyro_response.split(' ')[2][2::])
        print("Current angle: {}, Goal angle: {}".format(angle_gyro, angle_resultat))
        position = readGPS()
        result = position[1:4] + [angle_gyro]
        print('X:{} Y:{} Z:{} θ:{}'.format(result[0], result[1], result[2], result[3]))
        #print("Borne moins: {}, Borne plus: {}, angle_gyro < angle_resultat - 10: {}, angle_gyro > angle_resultat + 10: {}".format(angle_resultat-5, angle_resultat+5,angle_gyro < angle_resultat - 5,angle_gyro > angle_resultat + 5))
    move(0, 0)
    sleep(3)


def move(v1, v2):
    ser.write("{},{}".format(-v1,v2).encode('utf-8'))

def droitAuBut(x, y):
    borne = 0.1
    pos = readGPS()
    print("J'avance")
    move(100,100)
    flag = (pos[1] < x +borne and pos[1] > x -borne) and (pos[2] < y +borne and pos[2] > y -borne)
    print(flag)
    while not flag:
        print("x:{} y:{}".format(pos[1], pos[2]))
        flag = (pos[1] < x +borne and pos[1] > x -borne) and (pos[2] < y +borne and pos[2] > y -borne)
        pos = readGPS()
        sleep(0.1)
    move(0,0)
    print("Jsuis arrivé")
main()
