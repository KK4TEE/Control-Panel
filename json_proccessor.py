
# Code written by Seth Persigehl
# January 2014
# This is my first programing project, so consider it Alpha.
# There are a lot of comments because I am still new at this
# and might otherwise forget how specifically to do something.

# This program takes info from a JSON file on a website, formats it for
# an Arduino, and sends it out the serial port everytime the user presses
# enter. This should later be set to print every 200ms, but is set to user
# input while code is tested.

import time
import serial
import os
import linecache
import json
import urllib2
import math
import telemachus_plugin as tele
import config

url = config.url()

ser = serial.Serial(
    port=config.arduinoSerialPort(),
    #port='COM3',
    #baudrate=115200, # Causes the arduino buffer to fill up
    baudrate=9600, # Seems to be working well
   # parity=serial.PARITY_ODD,
   # stopbits=serial.STOPBITS_TWO,
   # bytesize=serial.SEVENBITS
)

gearStatus = 0
global gearStatus
brakeStatus = 0
global brakeStatus


def clamp(num, minn, maxn):
    if num < minn:
        return minn
    elif num > maxn:
        return maxn
    else:
        return num


#Arduino Utilities
def arduinoformat(inList):
 # Takes a list of numbers, rounds them as ints, and returns them as a string
 # Ideally this should be called only immedietely before transmission
    midlist = []
    for x in inList:
        midlist.append(int(round(float(x))))
    #midlist.append("\n")
    outstr = str(midlist)[1:-1]
    return outstr


def push_to_arduino(inputline):
    #ser.flushOutput()
    # Send data to the Arduino and end w/ a newline
    ser.write(inputline + '\n')
    #ser.write("255, 255, 255 \n")
    #time.sleep(.2)

def buttonHandler():
    global gearStatus
    global brakeStatus
    global memB
    global memBOLD
    if memB[1] == '1' and memB[1] != memBOLD[1]:
        if (memB[7] == '1'):  # Check the safety
            tele.stage()

    if memB[0] == '1' and memB[0] != memBOLD[0]:
        if memB[7] == '1':  # Check the safety
            tele.abort()

    if int(memB[2]) == 1 and memB[2] != memBOLD[2]:
        # Toggle gear based on what we did last time
        if gearStatus == 1:  # Telemachus does not yet read gear status
            tele.gear(0)
            gearStatus = 0
        elif gearStatus == 0:
            tele.gear(1)
            gearStatus = 1

    if int(memB[3]) == 1 and memB[3] != memBOLD[3]:
        # Toggle Light based on the Telemachus reading
        if tele.light(2) == 1:
            tele.light(0)
        elif tele.light(2) == 0:
            tele.light(1)

    if int(memB[4]) == 1 and memB[4] != memBOLD[4]:
        # Toggle brake based on what we did last time
        if brakeStatus == 1:  # Telemachus does not yet read brake status
            tele.brake(0)
            brakeStatus = 0
        elif brakeStatus == 0:
            tele.brake(1)
            brakeStatus = 1

    if int(memB[5]) == 1 and memB[5] != memBOLD[5]:
        # Toggle RCS based on the Telemachus reading
        if tele.rcs(2) == 1:
            tele.rcs(0)
        elif tele.rcs(2) == 0:
            tele.rcs(1)

    if int(memB[6]) == 1 and memB[6] != memBOLD[6]:
        # Toggle SAS based on the Telemachus reading
        if tele.sas(2) == 1:
            tele.sas(0)
        elif tele.sas(2) == 0:
            tele.sas(1)

#########################################################################
#Time to get started...
print 'Now starting program.'
print 'Warming up the Arduino...'
    # It took me hours to figure out I had to do this...
time.sleep(2)
print 'Starting main loop'

program_runtime = time.time()
arduino_sleep_marker = 0
button_sleep_marker = 0
memB = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
memBOLD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
n = 0


while 1:
    loop_start_time = time.time()

    climbgauge = tele.read_verticalspeed()
    if climbgauge > 0:
        climbgauge = clamp((int(4 * math.sqrt(climbgauge)) + 127), 0, 2255)
    elif climbgauge < 0:
        climbgauge = clamp((0 - int(4 * math.sqrt(
            abs(climbgauge))) + 127), 0, 255)
    else:
        climbgauge = 127  # Neutral

    memA = (str(int(round(tele.read_missiontime()))).zfill(8)
        + str(int(round(tele.read_asl()))).zfill(8)
        + str(int(round(tele.read_apoapsis()) / 100)).zfill(8)
        + str(int(round((tele.read_periapsis() / 100)))).zfill(8)
        + str(int(round(tele.read_verticalspeed()))).zfill(8)
        + chr(climbgauge) + 'BCDEFGH'
        )

    #arduinostring = [255, 255, 255]

    if arduino_sleep_marker > 0.2:
        try:
            print '.............'
            push_to_arduino(memA)
            print memA
        finally:
            arduino_sleep_marker = 0

    if ser.inWaiting > 9:
        serCharIn = str(ser.read(1))
        if serCharIn == '[':
            while n < 10:
                serCharIn = str(ser.read(1))
                if serCharIn == ']':
                    n = 0
                    ser.flushInput()
                    break
                else:
                    memB[n] = serCharIn
                n += 1
                if n == 11:
                    ser.flushInput()

    if button_sleep_marker > 0.1:
        buttonHandler()  # Reads memB for which buttons are pressed, then sends
                         # calls to telemachus as needed.
        button_sleep_marker = 0

        print memB
        print memBOLD
        memBOLD = list(memB)

    time.sleep(0.05)
    # This is used mostly to save CPU cycles and battery life of my laptop

    loop_end_time = time.time()
    loop_time = loop_end_time - loop_start_time
    arduino_sleep_marker += loop_time
    button_sleep_marker += loop_time

