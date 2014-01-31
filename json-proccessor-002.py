
# Code written by Seth Persigehl
# January 2014
# This is my first programing project, so consider it Alpha.
# There are a lot of comments because I am still new at this
# and might otherwise forget how specifically to do something.

#This program takes info from a CSV file, formats it for an Arduino, and sends
# it out the serial port everytime the user presses enter. This should later be
# set to print every 200ms, but is set to user input while code is tested.

import time
import serial
import os
import linecache
import json
import urllib2

# Configure the serial connections
  #That section can be coppied in right here

url = 'http://192.168.1.3:8085/telemachus/datalink?alt='
    # This is the URL that Telemachus can be found at.
    # Adjust it based on your firewall settings.


ser = serial.Serial(
    port='/dev/ttyACM0',
    #port='COM3',
    baudrate=57600,
    # hahaha 9600 is far too slow... the buffer fills up part way through
    # the write and then resets on the next loop. Lulz.
   # parity=serial.PARITY_ODD,
   # stopbits=serial.STOPBITS_TWO,
   # bytesize=serial.SEVENBITS
)


# Telemachus Definitions
    #The readings are for the active vessel unless otherwise noted
def read_angularvelocity():
    fresh_json = json.load(urllib2.urlopen(url + 'v.angularVelocity'))
    result = fresh_json["alt"]
    return result


def read_asl():
    fresh_json = json.load(urllib2.urlopen(url + 'v.altitude'))
    result = fresh_json[u'alt']
    return result


def read_apoapsis():
    fresh_json = json.load(urllib2.urlopen(url + 'o.ApA'))
    result = fresh_json["alt"]
    return result


def read_body():
    fresh_json = json.load(urllib2.urlopen(url + 'v.body'))
    result = fresh_json["alt"]
    return result


def read_eccentricity():
    fresh_json = json.load(urllib2.urlopen(url + 'o.eccentricity'))
    result = fresh_json["alt"]
    return result


def read_facing(dimension):
    if dimension in ['pitch']:
        fresh_json = json.load(urllib2.urlopen(url + 'n.pitch'))
        result = fresh_json["alt"]
    elif dimension in ['yaw']:
        fresh_json = json.load(urllib2.urlopen(url + 'n.heading'))
        result = fresh_json["alt"]
    elif dimension in ['roll']:
        fresh_json = json.load(urllib2.urlopen(url + 'n.roll'))
        result = fresh_json["alt"]
    else:
        result = -1
    return result


def read_heading():
    #Note: This returns facing:yaw, not your heading over land
    #Basically what the navball shows, not 'true' heading
    fresh_json = json.load(urllib2.urlopen(url + 'n.heading'))
    result = fresh_json["alt"]
    return result


def read_inclination():
    fresh_json = json.load(urllib2.urlopen(url + 'o.inclination'))
    result = fresh_json["alt"]
    return result


def read_missiontime():
    fresh_json = json.load(urllib2.urlopen(url + 'v.missionTime'))
    result = fresh_json["alt"]
    return result


def read_orbitalperiod():
    fresh_json = json.load(urllib2.urlopen(url + 'o.period'))
    result = fresh_json["alt"]
    return result


def read_orbitalvelocity():
    fresh_json = json.load(urllib2.urlopen(url + 'v.orbitalVelocity'))
    result = fresh_json["alt"]
    return result


def read_periapsis():
    fresh_json = json.load(urllib2.urlopen(url + 'o.PeA'))
    result = fresh_json["alt"]
    return result


def read_resource(resource):
    reformated_resource = url + 'r.resource' + '[' + resource + ']'
    fresh_json = json.load(urllib2.urlopen(reformated_resource))
    result = fresh_json["alt"]
    return result


def read_resource_max(resource):
    reformated_resource = url + 'r.resourceMax' + '[' + resource + ']'
    fresh_json = json.load(urllib2.urlopen(reformated_resource))
    result = fresh_json["alt"]
    return result


def read_surfacespeed():
    fresh_json = json.load(urllib2.urlopen(url + 'v.surfaceSpeed'))
    result = fresh_json["alt"]
    return result


def read_throttle():
    fresh_json = json.load(urllib2.urlopen(url + 'f.throttle'))
    result = fresh_json["alt"]
    return result


def read_universaltime():
    fresh_json = json.load(urllib2.urlopen(url + 't.universalTime'))
    result = fresh_json["alt"]
    return result


def read_verticalspeed():
    fresh_json = json.load(urllib2.urlopen(url + 'v.verticalSpeed'))
    result = fresh_json["alt"]
    return result


# Output Definitions


def set_pitch(pitch):
    #This is done by setting relative positions from 0 to 1, as a percent
    #This is based on the three bars in the lower left corner, NOT the Navball
    urllib2.urlopen(url + 'v.setPitch' + '[' + str(pitch) + ']')


def set_roll(roll):
    urllib2.urlopen(url + 'v.setRoll' + '[' + str(roll) + ']')


def set_yaw(yaw):
    urllib2.urlopen(url + 'v.setYaw' + '[' + str(yaw) + ']')


def toggle_ag(agn):
    urllib2.urlopen(url + 'f.ag' + agn)


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

print 'Now starting program.'
print 'Warming up the Arduino...'
    # It took me hours to figure out I had to do this...
time.sleep(2)
print 'Starting main loop'

program_runtime = time.time()
arduino_sleep_marker = 0


while 1:
    loop_start_time = time.time()


    arduinostring = [round(read_universaltime(), 2),
    read_throttle(),
    (round(read_asl()) / 70)]
    #arduinostring = [255, 255, 255]
    print arduinoformat(arduinostring)
    if arduino_sleep_marker > 0.2:
        push_to_arduino(arduinoformat(arduinostring))
        arduino_sleep_marker = 0




#    print read_facing('pitch'), read_facing('roll'), read_facing('yaw')
#    print (round(read_universaltime(), 2), read_throttle(), round(read_asl()),
#    round(read_periapsis()), round(read_apoapsis()), round(read_resource(
#    'LiquidFuel'), 3))

    set_pitch(0.2)
    set_roll(0)
    set_yaw(0)

    time.sleep(0.05)
    # This is used mostly to save CPU cycles and battery life of my laptop

    loop_end_time = time.time()
    loop_time = loop_end_time - loop_start_time
    arduino_sleep_marker += loop_time
    print ('Loop Time:' + str(loop_time) + 'Arduino:' + str(arduino_sleep_marker))
