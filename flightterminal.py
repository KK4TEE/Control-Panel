# python 2.7

# note: The data gathering portion of this should be centralized
# At the begining of each loop all needed data should be collected
# and then referenced as a local variable. I'll rewrite this when I
# get the chance.

# Notes on screen layout:
# Standard window block is ideally 25y by 15x chr
# Text display window is 25y by 30x chr
# Each gauge window is   25y by 15x including boarders
# Resource window is 10y by 15x
import math
import time
import curses
import copy
import telemachus_plugin as tele
import config

try:
    import serial
except:
    print 'PySerial does not seem to be installed'

try:
    ser = serial.Serial(
        port=config.arduinoSerialPort(),
        #port='COM3',
        #baudrate=115200, # Causes the arduino buffer to fill up
        baudrate=9600,  # Seems to be working well
       # parity=serial.PARITY_ODD,
       # stopbits=serial.STOPBITS_TWO,
       # bytesize=serial.SEVENBITS
    )
    arduinoConnected = True
    print 'Serial device connected at ' + config.arduinoSerialPort()
except:
    arduinoConnected = False
    print 'Unable to connect to arduino at ' + config.arduinoSerialPort()


def getFlightData(dIN):
    # Try to update the dictionary with live data. If any of it fails for any
    # reason, return the original dictionary and set the 'Radio Contact' key
    # to false.
    d = {'Zero': 0}
    try:
        d['MET'] = float(tele.read_missiontime())
        d['ASL'] = int(tele.read_asl())
        d['Body'] = str(tele.read_body())
        d['Ap'] = int(tele.read_apoapsis())
        d['Pe'] = int(tele.read_periapsis())
        d['Time to Ap'] = float(tele.read_time_to_ap())
        d['Time to Pe'] = float(tele.read_time_to_pe())
        d['Eccentricity'] = float(tele.read_eccentricity())
        d['Inclination'] = float(tele.read_inclination())
        d['Orbital Period'] = float(tele.read_orbitalperiod())
        d['Vertical Speed'] = float(tele.read_verticalspeed())

        d['SAS Status'] = int(tele.sas(2))
        if d['SAS Status'] == 1:
            d['SAS Status'] = True
        elif d['SAS Status'] == 0:
            d['SAS Status'] = False
        else:
            d['SAS Status'] = 'Error'
        d['RCS Status'] = int(tele.rcs(2))
        if d['RCS Status'] == 1:
            d['RCS Status'] = True
        else:
            d['RCS Status'] = False
        d['Light Status'] = int(tele.light(2))
        if d['Light Status'] == 1:
            d['Light Status'] = True
        else:
            d['Light Status'] = False

        d['ElectricCharge'] = float(tele.read_resource('ElectricCharge'))
        d['Max ElectricCharge'] = float(tele.read_resource_max(
            'ElectricCharge'))
        d['LiquidFuel'] = float(tele.read_resource('LiquidFuel'))
        d['Max LiquidFuel'] = float(tele.read_resource_max('LiquidFuel'))
        d['Oxidizer'] = float(tele.read_resource('Oxidizer'))
        d['Max Oxidizer'] = float(tele.read_resource_max('Oxidizer'))
        d['SolidFuel'] = float(tele.read_resource('SolidFuel'))
        d['Max SolidFuel'] = float(tele.read_resource_max('SolidFuel'))
        d['MonoPropellant'] = float(tele.read_resource('MonoPropellant'))
        d['Max MonoPropellant'] = float(tele.read_resource_max('MonoPropellant'))
        # If you are playing with realism mods, uncomment these as needed
        d['Oxygen'] = float(tele.read_resource('Oxygen'))
        d['Max Oxygen'] = float(tele.read_resource_max('Oxygen'))
        d['LiquidOxygen'] = float(tele.read_resource('LiquidOxygen'))
        d['Max LiquidOxygen'] = float(tele.read_resource_max('LiquidOxygen'))
        d['LiquidH2'] = float(tele.read_resource('LiquidH2'))
        d['Max LiquidH2'] = float(tele.read_resource_max('LiquidH2'))


        d['Previous Radio Contact'] = dIN['Radio Contact']
        d['Radio Contact'] = True
        return d

    except:
        dIN['Previous Radio Contact'] = dIN['Radio Contact']
        dIN['Radio Contact'] = False
        del d
        return dIN


def drawPrimaryStatusWindow(yCord, xCord):
    primaryStatusW = myscreen.subwin(25, 30, yCord, xCord)
    primaryStatusW.border()
    yL = 0  # local variable for the Y line
    #xL = 0  # local variable for the X line
    primaryStatusW.addstr(yL, 1, "##      Earth Time:       ##", curses.A_STANDOUT)
    yL += 1
    primaryStatusW.addstr(yL, 2, time.strftime("%a, %d %b %Y %H:%M:%S"), curses.color_pair(1))
    yL += 1
    yL += 1
    primaryStatusW.addstr(yL, 1, "##     Mission Time:      ##", curses.A_STANDOUT)
    yL += 1
    primaryStatusW.addstr(yL, 4, str(round(fd['MET'], 1))
        .zfill(21), curses.color_pair(1))
    yL += 1
    yL += 1

    primaryStatusW.addstr(yL, 1, "Body: ")
    primaryStatusW.addstr(yL, 20, str(fd['Body']).rjust(8))
    yL += 1
    primaryStatusW.addstr(yL, 1, "ASL:")
    primaryStatusW.addstr(yL, 20, str(fd['ASL'])
        .zfill(filldigits))
    yL += 1
    yL += 1

    primaryStatusW.addstr(yL, 1, "##  Orbital Information   ##", curses.A_STANDOUT)
    yL += 1
    primaryStatusW.addstr(yL, 1, "Apoapsis:")
    primaryStatusW.addstr(yL, 20, str(fd['Ap'])
        .zfill(filldigits))
    yL += 1
    primaryStatusW.addstr(yL, 1, "Periapsis:")
    primaryStatusW.addstr(yL, 20, str(fd['Pe'])
        .zfill(filldigits))
    yL += 1
    primaryStatusW.addstr(yL, 1, "Eccentricity:")
    primaryStatusW.addstr(yL, 20, str(round(fd['Eccentricity'], 6))
        .zfill(filldigits))
    yL += 1
    primaryStatusW.addstr(yL, 1, "Inclination:")
    primaryStatusW.addstr(yL, 20, str(round(fd['Inclination'], 6))
        .zfill(filldigits))
    yL += 1
    primaryStatusW.addstr(yL, 1, "Orbital Period:")
    primaryStatusW.addstr(yL, 20, str(round(fd['Orbital Period'], 1))
        .zfill(filldigits))
    yL += 1
    primaryStatusW.addstr(yL, 1, "Time to Ap:")
    primaryStatusW.addstr(yL, 20, str(round(fd['Time to Ap'], 1))
        .zfill(filldigits))
    yL += 1
    primaryStatusW.addstr(yL, 1, "Time to Pe:")
    primaryStatusW.addstr(yL, 20, str(round(fd['Time to Pe'], 1))
        .zfill(filldigits))
    yL += 1
    yL += 1

    primaryStatusW.addstr(yL, 1, "##  Flight Configuration  ##",
         curses.A_STANDOUT)
    yL += 1
    primaryStatusW.addstr(yL, 1, "SAS Status:")
    primaryStatusW.addstr(yL, 20, str(fd['SAS Status']).ljust(5))
    yL += 1
    primaryStatusW.addstr(yL, 1, "RCS Status:")
    primaryStatusW.addstr(yL, 20, str(fd['RCS Status']).ljust(5))
    yL += 1
    primaryStatusW.addstr(yL, 1, "Ext. Lights:")
    primaryStatusW.addstr(yL, 20, str(fd['Light Status']).ljust(5))
    yL += 1
    primaryStatusW.addstr(yL, 1, "Landing Gear:")
    primaryStatusW.addstr(yL, 20, str(ps['Gear Status']).ljust(5))
    yL += 1
    primaryStatusW.addstr(yL, 1, "Brake Status:")
    primaryStatusW.addstr(yL, 20, str(ps['Brake Status']).ljust(5))
    yL += 1
    return yL


def drawResourceWindow(yCord, xCord):
    resourceW = myscreen.subwin(10, 30, yCord, xCord)
    resourceW.border()
    yL = 0  # local variable for the Y line
    #xL = 0  # local variable for the X line
    resourceW.addstr(yL, 1, "##       Resources        ##",
        curses.A_STANDOUT)
    yL += 1
    if fd['ElectricCharge'] != -1:
        resourceW.addstr(yL, 1, "Electricity:")
        resourceW.addstr(yL, 20, str(int(fd['ElectricCharge']))
            .zfill(filldigits))
        yL += 1
    if fd['Oxygen'] != -1:
        resourceW.addstr(yL, 1, "Oxygen:")
        resourceW.addstr(yL, 20, str(int(fd['Oxygen']))
            .zfill(filldigits))
        yL += 1
    if fd['MonoPropellant'] != -1:
        resourceW.addstr(yL, 1, "MonoPropellant:")
        resourceW.addstr(yL, 20, str(int(fd['MonoPropellant']))
            .zfill(filldigits))
        yL += 1
    if fd['LiquidFuel'] != -1:
        resourceW.addstr(yL, 1, "Liquid Fuel:")
        resourceW.addstr(yL, 20, str(int(fd['LiquidFuel']))
            .zfill(filldigits))
        yL += 1
    if fd['Oxidizer'] != -1:
        resourceW.addstr(yL, 1, "Oxidizer:")
        resourceW.addstr(yL, 20, str(int(fd['Oxidizer']))
            .zfill(filldigits))
        yL += 1
    if fd['SolidFuel'] != -1:
        resourceW.addstr(yL, 1, "Solid Fuel:")
        resourceW.addstr(yL, 20, str(int(fd['SolidFuel']))
            .zfill(filldigits))
        yL += 1
    if fd['LiquidH2'] != -1:
        resourceW.addstr(yL, 1, "Liquid Hydrogen:")
        resourceW.addstr(yL, 20, str(int(fd['LiquidH2']))
            .zfill(filldigits))
        yL += 1
    if fd['LiquidOxygen'] != -1:
        resourceW.addstr(yL, 1, "Liquid Oxygen:")
        resourceW.addstr(yL, 20, str(int(fd['LiquidOxygen']))
            .zfill(filldigits))
        yL += 1

    return yL


def drawArduinoWindow(yCord, xCord):
    arduinoW = myscreen.subwin(10, 60, yCord, xCord)
    arduinoW.border()
    yL = 0  # local variable for the Y line
    #fNorm = curses.A_NORMAL  # Formatting for unselected options
    arduinoW.addstr(yL, 30 - 12, "##  Arduino Readouts  ##",
        curses.A_STANDOUT)
    yL += 1
    arduinoW.addstr(yL, 1, "Serial Out:")
    yL += 1
    try:
        arduinoW.addstr(yL, 1, str(memA))
    except:
        arduinoW.addstr(yL, 1,
        'Memory contains bytes that can not be printed    ')
    yL += 1
    yL += 1
    arduinoW.addstr(yL, 1, "Serial In:")
    # arduinoW.addstr(yL, 10, str(int(str(memB))))
    yL += 1
    arduinoW.addstr(yL, 1, "".join([str(x) for x in memB]))
    yL += 1
    yL += 1
    arduinoW.addstr(yL, 1, "Program Loop Time:")
    yL += 1
    arduinoW.addstr(yL, 1, str(round(loopTime, 5)))
    yL += 1


def drawMainMenu(yCord, xCord):
    menuDepth = 15
    mainMenu = myscreen.subwin(menuDepth, 25, yCord, xCord)
    mainMenu.clear()
    mainMenu.attron(curses.color_pair(3))
    mainMenu.border()
    mainMenu.attroff(curses.color_pair(3))
    #mainMenu.bkgd(32, curses.color_pair(2))  #Fill the background with spaces
    yL = 1  # local variable for the Y line
    FSO = curses.A_STANDOUT  # Formatting for selected option

    mainMenu.addstr(0, 12 - 5, " Main Menu ",
        curses.A_BOLD)
    if ps['Main Menu Selection'] == yL:
            mainMenu.addstr(yL, 1, str(yL) + ":Toggle Flight Data", FSO)
            if chrin == ord('\n'):
                myscreen.clear()
                if ps['Flight Transceiver Active'] is True:
                    ps['Flight Transceiver Active'] = False
                elif ps['Flight Transceiver Active'] is False:
                    ps['Flight Transceiver Active'] = True
    else:
            mainMenu.addstr(yL, 1, str(yL) + ":Toggle Flight Data")

    yL += 1

    if arduinoConnected is True:
        if ps['Main Menu Selection'] == yL and ps['Arduino Active'] is False:
            mainMenu.addstr(yL, 1, str(yL) + ":Activate Arduino", FSO)
            if chrin == ord('\n'):
                ps['Arduino Active'] = True
                ps['Arduino Active'] = True
        elif ps['Main Menu Selection'] != yL and ps['Arduino Active'] is False:
            mainMenu.addstr(yL, 1, str(yL) + ":Activate Arduino")
        elif ps['Main Menu Selection'] == yL and ps['Arduino Active'] is True:
            mainMenu.addstr(yL, 1, str(yL) + ":Deactivate Arduino", FSO)
            if chrin == ord('\n'):
                ps['Arduino Active'] = False
        elif ps['Main Menu Selection'] != yL and ps['Arduino Active'] is True:
            mainMenu.addstr(yL, 1, str(yL) + ":Deactivate Arduino")
        else:
            pass
    elif arduinoConnected is False:
        mainMenu.attron(curses.color_pair(2))
        if ps['Main Menu Selection'] == yL:
            mainMenu.addstr(yL, 1, str(yL) + ":Arduino not available", FSO)
        else:
            mainMenu.addstr(yL, 1, str(yL) + ":Arduino not available")
        mainMenu.attroff(curses.color_pair(2))

    if ps['Arduino Active'] is True:
        yL += 1
        if ps['Main Menu Selection'] == yL:
                mainMenu.addstr(yL, 1, str(yL) + ":Arduino - Flight Mode", FSO)
                if chrin == ord('\n'):
                    arduino['Display Mode'] = 'Flight Mode'
        else:
                mainMenu.addstr(yL, 1, str(yL) + ":Arduino - Flight Mode")
        yL += 1
        if ps['Main Menu Selection'] == yL:
                mainMenu.addstr(yL, 1, str(yL) + ":Arduino - Clock Mode", FSO)
                if chrin == ord('\n'):
                    arduino['Display Mode'] = 'Clock'
        else:
                mainMenu.addstr(yL, 1, str(yL) + ":Arduino - Clock Mode")
        yL += 1
        if ps['Main Menu Selection'] == yL:
                mainMenu.addstr(yL, 1, str(yL) + ":Arduino - Lamp Test", FSO)
                if chrin == ord('\n'):
                    arduino['Display Mode'] = 'Lamp Test'
        else:
                mainMenu.addstr(yL, 1, str(yL) + ":Arduino - Lamp Test")
        yL += 1

    yL += 1
    if ps['Main Menu Selection'] == yL:
            mainMenu.addstr(yL, 1, str(yL) + ":Force Screen Redraw", FSO)
            if chrin == ord('\n'):
                myscreen.clear()
    else:
            mainMenu.addstr(yL, 1, str(yL) + ":Force Screen Redraw")

    yL += 1
    if ps['Main Menu Selection'] == yL:  # Exit doesn't actually work yet
            mainMenu.addstr(yL, 1, str(yL) + ":Exit", FSO)
            if chrin == ord('\n'):
                pass
    else:
            mainMenu.addstr(yL, 1, str(yL) + ":Exit")

    mainMenu.addstr(menuDepth - 4, 2, "Press Enter to Select")
    mainMenu.addstr(menuDepth - 3, 1, "Program Loop Time:")
    mainMenu.addstr(menuDepth - 2, 1, str(round(loopTime, 5)))

    #### Keyboard input for moving the hightlight ###
    if chrin == ord('1'):
        ps['Main Menu Selection'] = 1
    elif chrin == ord('2'):
        ps['Main Menu Selection'] = 2
    elif chrin == ord('3'):
        ps['Main Menu Selection'] = 3
    elif chrin == ord('4'):
        ps['Main Menu Selection'] = 4
    elif chrin == ord('5'):
        ps['Main Menu Selection'] = 5
    elif chrin == ord('6'):
        ps['Main Menu Selection'] = 6

    elif chrin == 258:
        if ps['Main Menu Selection'] < yL:
            ps['Main Menu Selection'] += 1
        else:
            ps['Main Menu Selection'] = 1
    elif chrin == 259:
        if ps['Main Menu Selection'] > 1:
            ps['Main Menu Selection'] -= 1
        else:
            ps['Main Menu Selection'] = yL
    elif chrin == ord('\n'):
        ps['Main Menu is Open'] = False
        ps['Slection Made'] = True
        mainMenu.clear()
    elif chrin == 27:
        ps['Main Menu is Open'] = False
        ps['Slection Made'] = False
        mainMenu.clear()
    elif chrin == 96:
        ps['Main Menu is Open'] = False
        ps['Slection Made'] = False
        mainMenu.clear()


def formatRCC(inputln):  # Formating Reading Color Critical
    if int(inputln) < 0:
        inputln = str(int(inputln)).zfill(filldigits)
        return inputln, curses.color_pair(2)
    else:
        return str(int(inputln)).zfill(filldigits)


def drawVGauge(gLabel, resource, yCord, xCord):
    # Draws a gauge from 0-100% that is 30 rows x 15 Coll with the top left
    # corner at (yCord, xCord)
    percentVal = round((fd[resource] /
        fd[str('Max ' + resource)]) * 100, 1)
    if percentVal >= 100:
        percentVal = int(100)
    gauge = myscreen.subwin(25, 15, yCord, xCord)
    gauge.clear()
    gauge.border()
    gauge.addstr(0, 7 - len(gLabel) / 2, gLabel)
    barHeight = min(20, int(percentVal / 5))
    gauge.addstr(22, 7 - len(gLabel) / 2, gLabel)
    if barHeight > 0:
        for n in range(-1, 2):  # Make a vline 3 colums wide
            if barHeight > 0:
                gauge.attron(curses.color_pair(3))
                gauge.vline(22 - barHeight, 7 + n, curses.ACS_CKBOARD,
                    barHeight)
                gauge.attroff(curses.color_pair(3))
            if barHeight >= 5:
                gauge.attron(curses.color_pair(2))
                gauge.vline(22 - barHeight, 7 + n, curses.ACS_CKBOARD,
                    barHeight - 5)
                gauge.attroff(curses.color_pair(2))
            if barHeight > 10:
                gauge.attron(curses.color_pair(1))
                gauge.vline(22 - barHeight, 7 + n, curses.ACS_CKBOARD,
                    barHeight - 10)
                gauge.attroff(curses.color_pair(1))
        gauge.addstr(23, 5, str(percentVal).zfill(3) + '%')
    elif percentVal < 5 and percentVal > 0:
        gauge.attron(curses.color_pair(3))
        gauge.addstr(23, 6, 'Low')
        gauge.attroff(curses.color_pair(3))
    elif percentVal == 0:
        gauge.attron(curses.color_pair(3))
        gauge.addstr(23, 5, 'Empty')
        gauge.attroff(curses.color_pair(3))
    else:
        gauge.addstr(23, 1, 'Not Available')


###  Arduino Utilities
def push_to_arduino(inputline):
    #ser.flushOutput()
    # Send data to the Arduino and end w/ a newline
    ser.write(inputline + '\n')
    #ser.write("255, 255, 255 \n")
    #time.sleep(.2)


def formatForArduino(mode):

    if mode == 'Lamp Test':  # Light Test
        arduino['7r0 Data'] = '88888888'
        arduino['7r1 Data'] = '88888888'
        arduino['7r2 Data'] = '88888888'
        arduino['7r3 Data'] = '88888888'
        arduino['7r4 Data'] = '88888888'
        arduino['g0 Data'] = chr(255)
        arduino['g1 Data'] = chr(255)
        arduino['g2 Data'] = chr(255)
        arduino['g3 Data'] = chr(255)
        arduino['g4 Data'] = chr(255)
        arduino['g5 Data'] = chr(255)
        arduino['g6 Data'] = chr(255)
        arduino['g7 Data'] = chr(255)

    elif mode == 'Clock':
        '''There's something weird going on here that causes the code to
        take a full 300ms or so to loop. This requires further research.'''
        arduino['7r0 Data'] = '        '
        arduino['7r1 Data'] = str(time.strftime("%H %M %S"))
        arduino['7r2 Data'] = str(time.strftime(" %m  %d "))
        arduino['7r3 Data'] = str(time.strftime("  %Y  "))
        arduino['7r4 Data'] = '        '
        arduino['g0 Data'] = '0'
        arduino['g1 Data'] = '0'
        arduino['g2 Data'] = '0'
        arduino['g3 Data'] = '0'
        arduino['g4 Data'] = '0'
        arduino['g5 Data'] = '0'
        arduino['g6 Data'] = '0'
        arduino['g7 Data'] = '0'
    else:
        arduino['7r0 Data'] = str(int(round(fd["MET"]))).zfill(8)
        arduino['7r1 Data'] = str(int(round(fd["ASL"] / 100))).zfill(8)
        arduino['7r2 Data'] = str(int(round(fd["Ap"] / 100))).zfill(8)
        arduino['7r3 Data'] = str(int(round(fd["Pe"] / 100))).zfill(8)
        arduino['7r4 Data'] = str(int(round(fd["Time to Ap"]))).zfill(8)
        arduino['g0 Data'] = 'A'
        arduino['g1 Data'] = 'A'
        arduino['g2 Data'] = 'A'
        arduino['g3 Data'] = 'A'
        arduino['g4 Data'] = 'A'
        arduino['g5 Data'] = 'A'
        arduino['g6 Data'] = 'A'
        arduino['g7 Data'] = 'A'


def buttonHandler():
    # Reads memB for which buttons are pressed, then sends
    # calls to telemachus as needed.
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
        if ps['Gear Status'] is True:
            # Telemachus does not yet read gear status
            tele.gear(0)
            ps['Gear Status'] = False
        elif ps['Gear Status'] is False:
            tele.gear(1)
            ps['Gear Status'] = True

    if int(memB[3]) == 1 and memB[3] != memBOLD[3]:
        # Toggle Light based on the Telemachus reading
        if fd['Light Status'] is True:
            tele.light(0)
        elif fd['Light Status'] is False:
            tele.light(1)

    if int(memB[4]) == 1 and memB[4] != memBOLD[4]:
        # Toggle brake based on what we did last time
        if ps['Brake Status'] is True:
            # Telemachus does not yet read brake status
            tele.brake(0)
            ps['Brake Status'] = False
        elif ps['Brake Status'] is False:
            tele.brake(1)
            ps['Brake Status'] = True

    if int(memB[5]) == 1 and memB[5] != memBOLD[5]:
        # Toggle RCS based on the Telemachus reading
        if fd['RCS Status'] is True:
            tele.rcs(0)
        elif fd['RCS Status'] is False:
            tele.rcs(1)

    if int(memB[6]) == 1 and memB[6] != memBOLD[6]:
        # Toggle SAS based on the Telemachus reading
        if fd['SAS Status'] is True:
            tele.sas(0)
        elif fd['SAS Status'] is False:
            tele.sas(1)


def clamp(num, minn, maxn):
    if num < minn:
        return minn
    elif num > maxn:
        return maxn
    else:
        return num


#### Main Program ############################################################
myscreen = curses.initscr()
if curses.can_change_color:
    curses.start_color()
    curses.use_default_colors()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)


curses.noecho()
curses.cbreak()

myscreen.keypad(1)

chrin = -1
filldigits = 8
arduinoActive = 0
menuOpen = 0

# Flight Data Memory and other variables
fd = {  # Primary data storage
'MET': -1, 'ASL': -1, 'Ap': -1, 'Pe': -1, 'Time to Ap': -1, 'Time to Pe': -1,
'Eccentricity': -1, 'Inclination': -1, 'Orbital Period': -1,
'Vertical Speed': -1, 'SAS Status': -1, 'RCS Status': -1, 'Light Status': -1,
'ElectricCharge': -1, 'Max ElectricCharge': -1,
'LiquidFuel': -1, 'Max LiquidFuel': -1,
'Oxidizer': -1, 'Max Oxidizer': -1,
'SolidFuel': -1,'Max SolidFuel': -1,
'MonoPropellant': -1, 'Max MonoPropellant': -1,
'Oxygen': -1, 'Max Oxygen': -1,  # Realisim Resources
'LiquidH2': -1, 'Max LiquidH2': -1,
'LiquidOxygen': -1, 'Max LiquidOxygen': -1,
'Radio Contact': False, 'Previous Radio Contact': False}

ps = {  # Program Settings
'Main Menu is Open': False, 'Main Menu Selection': 1, 'Slection Made': False,
'Flight Transceiver Active': False,
'Terminal Max Y': 25, 'Terminal Max X': 40,
'Arduino Sleep Marker': 0, 'Arduino Active': False, 'Button Sleep Marker': 0,
'flightData Sleep Marker': 0, 'Gear Status': False, 'Brake Status': False}

arduino = {  # Arduino Configurtion, using rows
'Display Mode': 'Lamp Test',
'7r0 Name': 'MET', '7r0 Data': str().zfill(8),
'7r1 Name': 'ASL', '7r1 Data': str().zfill(8),
'7r2 Name': 'Ap', '7r2 Data': str().zfill(8),
'7r3 Name': 'Pe', '7r3 Data': str().zfill(8),
'7r4 Name': 'Time to Ap', '7r4 Data': str().zfill(8),
'g0 Name': 'MET', 'g0 Data': str().zfill(1)
}
arduinoSleepMarker = 0
buttonSleepMarker = 0
flightDataSleepMarker = config.pollInterval()
memB = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Current serial input
memBOLD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Old serial input
n = 0
ps['Terminal Max Y'], ps['Terminal Max X'] = myscreen.getmaxyx()

print ps['Terminal Max Y']
print ps['Terminal Max X']

### Flight Computer Section ##################################################
while chrin != 48:  # Loop until the user presses the Zero key
    loopStartTime = time.time()
    if (ps['Terminal Max Y'], ps['Terminal Max X']) != myscreen.getmaxyx():
        myscreen.clear()
    if ps['Flight Transceiver Active'] is True:
        if flightDataSleepMarker >= config.pollInterval() and (
            fd['Radio Contact'] is True):
            fd = getFlightData(fd)
            flightDataSleepMarker = 0
    #### Expand this into an actual error handling bit.
    # Do a single test once per second that only polls one item
    # Alternativel, do actually multithreading w/ the URL stuff in the other
    # thread. That makes far more sense.
        elif flightDataSleepMarker >= config.pollInterval() + 2:
            fd = getFlightData(fd)
            flightDataSleepMarker = 0

    myscreen.border()
    ps['Terminal Max Y'], ps['Terminal Max X'] = myscreen.getmaxyx()
    yLine = 2  # Starting Row for flight info
    myscreen.nodelay(1)
    myscreen.addstr(0, ps['Terminal Max X'] / 2 - 12, "Persigehl Flight Terminal")

    if fd['Radio Contact'] is True and fd['Previous Radio Contact'] is True:
        drawPrimaryStatusWindow(1, 1)
        drawResourceWindow(26, 1)
    elif fd['Radio Contact'] is False:
        myscreen.addstr(ps['Terminal Max Y'] - 2, ps['Terminal Max X'] / 2 - 12,
            "### Radio Contact Lost ###", curses.A_STANDOUT)
    elif fd['Radio Contact'] is True and fd['Previous Radio Contact'] is False:
        myscreen.clear()
        myscreen.border()
        drawPrimaryStatusWindow(1, 1)
        drawResourceWindow(26, 1)

    #myscreen.vline(20, 35, curses.ACS_CKBOARD, 4)
    #drawVGauge("Test Gauge", 42, 1, 35)
    if fd['ElectricCharge'] != -1:
        drawVGauge("Electricity", 'ElectricCharge', 1, 31)

    if fd['Oxygen'] != -1:
        drawVGauge("Oxygen", 'Oxygen', 1, 61)

    if fd['MonoPropellant'] != -1:
        drawVGauge("MonoProp.", 'MonoPropellant', 1, 46)

    if fd['LiquidFuel'] != -1:
        drawVGauge("LiquidFuel", 'LiquidFuel', 1, 61)

    if fd['Oxidizer'] != -1:
        drawVGauge("Oxidizer", 'Oxidizer', 1, 61)


    if fd['LiquidH2'] != -1:
        drawVGauge("Liquid H2", 'LiquidH2', 1, 76)

    if fd['LiquidOxygen'] != -1:
        drawVGauge("Liquid Oxygen", 'LiquidOxygen', 1, 91)

### Arduino Section ##########################################################

    if ps['Arduino Active'] is True:
        climbgauge = int(fd['Vertical Speed'])
        '''This will need to be rewritten to only allow a subset of characters
        so that it will no longer be possible to get header characters mixed
        up in the trasmission (ie: '[' or ']') Perhaps limit the ranges to
        only 128 bits, which is more than the gauges I have can really
        support anyways.'''
        if climbgauge > 0:
            climbgauge = clamp((int(4 * math.sqrt(climbgauge)) + 127), 0, 254)
        elif climbgauge < 0:
            climbgauge = clamp((0 - int(4 * math.sqrt(
                abs(climbgauge))) + 127), 0, 254)
        else:
            climbgauge = 127  # Neutral

        formatForArduino(arduino['Display Mode'])
        memA = (
            str(arduino['7r0 Data']) +
            str(arduino['7r1 Data']) +
            str(arduino['7r2 Data']) +
            str(arduino['7r3 Data']) +
            str(arduino['7r4 Data']) +
            str(arduino['g0 Data']) +
            str(arduino['g1 Data']) +
            str(arduino['g2 Data']) +
            str(arduino['g3 Data']) +
            str(arduino['g4 Data']) +
            str(arduino['g5 Data']) +
            str(arduino['g6 Data']) +
            str(arduino['g7 Data'])
            )

        if arduinoSleepMarker > 0.25:
            try:
                push_to_arduino(memA)
            except:
                pass
            finally:
                arduinoSleepMarker = 0

        if ser.inWaiting > 9:
            try:
                serCharIn = str(ser.read(1))
                if serCharIn == '[':
                    while n < 12:
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
            except:
                ser.flushInput()

        if buttonSleepMarker > 0.1:
            buttonHandler()
            button_sleep_marker = 0
            memBOLD = list(memB)

        drawArduinoWindow(26, 31)

    if chrin == 96 and ps['Main Menu is Open'] is False:
    # Display the pop up menu if '`' is pressed (the key to the left of 1)
        ps['Main Menu is Open'] = True
        chrin = 0

    if ps['Main Menu is Open'] is True:
        drawMainMenu(1, ps['Terminal Max X'] - 26)

### Main Loop Cleanup ########################################################
    myscreen.addstr(ps['Terminal Max Y'] - 1, 2, " Press ` to toggle Main Menu ")
    myscreen.addstr(ps['Terminal Max Y'] - 1, ps['Terminal Max X'] - 19, " Press 0 to Exit ")
    myscreen.refresh()
    chrin = myscreen.getch()

    loopTimeOffset = 0.05 + loopStartTime - time.time()
        # This can be used to slow the entire program down to cycle at a
        # given interval. This is a failsafe to prevent 100% utilization
    if loopTimeOffset > 0:
        time.sleep(loopTimeOffset)
    # Combined Bandwidth used based on interval:
    # 33ms = around 395 Packets/S, 345kbs
    # 25ms = around 500 Packets/S, 410kbs
    loopEndTime = time.time()
    loopTime = loopEndTime - loopStartTime
    arduinoSleepMarker += loopTime
    buttonSleepMarker += loopTime
    flightDataSleepMarker += loopTime


curses.nocbreak()
myscreen.keypad(0)
curses.echo()
curses.endwin()
print 'FlightTerminal ended by user'
print 'Screen dimensions on close were:'
print ('Y: ' + str(ps['Terminal Max Y']) + " " + 'X: ' +
    str(ps['Terminal Max X']))
