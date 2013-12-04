# Code written by Seth Persigehl 
# November 2013
# This is my first programing project, so consider it Alpha.
# There are a lot of comments because I am still new at this
# and might otherwise forget how specifically to do something.

#This program takes info from a CSV file, formats it for an Arduino, and sends it out the serial port everytime the user presses enter. This should later be set to print every 200ms, but is set to user input while code is tested.

import time
import serial
import os
import linecache

####These are presets for swithing between Windows and Linux, as well as kOS vs Flight Recorder ###
#logdir = "/home/seth/.local/share/Steam/SteamApps/common/Kerbal Space Program/GameData/FlightRecorder/Plugins/PluginData/FlightRecorder/"
#logdir = "/home/seth/.local/share/Steam/SteamApps/common/Kerbal Space Program/Plugins/PluginData/Archive/"
#logdir = "C:\Program Files (x86)\Steam\steamapps\common\Kerbal Space Program\Plugins\PluginData\Archive\\"
logdir = "C:\Program Files (x86)\Steam\steamapps\common\Kerbal Space Program\GameData\FlightRecorder\Plugins\PluginData\FlightRecorder\\"

# Configure the serial connections
# Be sure to change these to suit your particular device(s)
ser = serial.Serial(
    #port='/dev/ttyACM0',
    port='COM3',
    baudrate=9600,
   # parity=serial.PARITY_ODD,
   # stopbits=serial.STOPBITS_TWO,
   # bytesize=serial.SEVENBITS
)


######## Definitions ########################
def firstline(filename):
 # This reads the first line of a CSV file and returns it as a list
    firstlineraw = linecache.getline(filename,1)
 # Seperate the list by commas
    firstlist = firstlineraw.split(", ") 
 # Remove the \n at the end of the line 
    firstlist[-1] = firstlist[-1].strip()
    return firstlist


def lastline(filename):
  # Reads the last line of the file (filename) and returns it.  
    offset = 0
    with open(filename) as f:
        while 1:
            f.seek(offset, 2)
            if f.tell() == 0:
                return f.read().strip()
                
            line = f.read()
            if line.strip() and line[0] == '\n':
                return line.strip()

            offset -= 1 


def format_as_dict(firstlist,lastlist):
 # Takes two lists and zips them into a dictionary
    firststr = ''.join(firstlist)
    firstproper = firststr.split(",")
    
    laststr = ''.join(lastlist)
    lastproper = laststr.split(",")

    finaldict = dict(zip(firstproper,lastproper))
    return finaldict


def arduinoformat(inList):
 # Takes a list of numbers, rounds them as ints, and returns them as a string
 # Ideally this should be called only immedietely before transmission
    midlist = []
    for x in inList:
        midlist.append(int(round(float(x))))
    #midlist.append("\n")
    outstr = str(midlist)[1:-1]
    return outstr


def find_most_recent(directory, partial_file_name):
 #Searches the (directory) for the latest newest file that contains (partial_file_name)
   # list all the files in the directory
    files = os.listdir(directory)
   # remove all file names that don't match partial_file_name string
    files = filter(lambda x: x.find(partial_file_name) > -1, files)
   # create a dict that contains list of files and their modification timestamps
    name_n_timestamp = dict([(x, os.stat(directory+x).st_mtime) for x in files])
   # return the file with the latest timestamp
    return max(name_n_timestamp, key=lambda k: name_n_timestamp.get(k))


def update_filepath():
   #Determine the most recent log file containing "some_string" in the name
    recentfile = find_most_recent(logdir,"csv")
   # Format the file path into the proper OS specific path
    return os.path.join(logdir,recentfile)


######## Begin the main program ############
while 1 :
   # The File path should probably only be updatedevery 30s or so
   # Make this a definition and call it instead
    absfilepath = update_filepath()
    flightdata = format_as_dict(firstline(absfilepath),lastline(absfilepath))

# Format  data for the Arduino to read. 
# Do the heavy lifting in python, not as a sketch.
   # Set the geeForce gauge to peak at 15G's
    flightdata['geeForce_immediate'] = 17 * float(flightdata['geeForce_immediate'])
   # Set altitutde 8 bit peak to 100km
    flightdata['altitude'] = float(flightdata['altitude']) / 392
   # Set atmDensity to a percent of 255. It may be desireable to use a log scale instead of linear.
    convertedAtmDensity = float(flightdata['atmDensity']) * 255
    flightdata['atmDensity'] = str(convertedAtmDensity) 


   # Begin final I/O stuff
    arduinostring = [flightdata['geeForce_immediate'], flightdata['altitude'], flightdata['atmDensity']]
   ## arduinostring = [flightdata['Fuel'], flightdata['ElectricCharge'], flightdata['Altitude']]

    print arduinoformat(arduinostring)
       # Send data to the Arduino and end w/ a newline
 # Keyboard Loop: Depending on how advanced I want to get with options for this program it might be a better option to simply remove kayboard input and simply loop every 200ms.
    # get keyboard input
    input = raw_input(">> ")
        # Python 3 users
        # input = input(">> ")
    if input == 'exit':
        ser.close()
        exit()
    else: 
       # Send data to the Arduino and end w/ a newline
        ser.write(arduinoformat(arduinostring) + '\n')
        out = ''
       # Wait 200ms for a reply from the Arduino
        time.sleep(0.2)
        while ser.inWaiting() > 0:
            out += ser.read(1)

        if out != '':
            print ">>" + out
 
