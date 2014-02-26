# python 2.7

# note: The data gathering portion of this should be centralized
# At the begining of each loop all needed data should be collected
# and then referenced as a local variable. I'll rewrite this when I
# get the chance.
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
        baudrate=9600, # Seems to be working well
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
        d['Ap'] = int(tele.read_apoapsis())
        d['Pe'] = int(tele.read_periapsis())
        d['Time to Ap'] = float(tele.read_time_to_ap())
        d['Time to Pe'] = float(tele.read_time_to_pe())
        d['Eccentricity'] = float(tele.read_eccentricity())
        d['Inclination'] = float(tele.read_inclination())
        d['Orbital Period'] = float(tele.read_orbitalperiod())
        d['Vertical Speed'] = float(tele.read_verticalspeed())

        d['SAS Status'] = int(tele.sas(2))
        d['RCS Status'] = int(tele.rcs(2))
        d['Light Status'] = int(tele.light(2))

        d['ElectricCharge'] = float(tele.read_resource('ElectricCharge'))
        d['Max ElectricCharge'] = float(tele.read_resource_max(
            'ElectricCharge'))
        d['LiquidFuel'] = float(tele.read_resource('LiquidFuel'))
        d['Max LiquidFuel'] = float(tele.read_resource_max('LiquidFuel'))
        d['Oxidizer'] = float(tele.read_resource('Oxidizer'))
        d['MaxOxidizer'] = float(tele.read_resource_max('Oxidizer'))
        d['SolidFuel'] = float(tele.read_resource('SolidFuel'))
        d['Max SolidFuel'] = float(tele.read_resource_max('SolidFuel'))

        d['Previous Radio Contact'] = dIN['Radio Contact']
        d['Radio Contact'] = True
        return d

    except:
        dIN['Previous Radio Contact'] = dIN['Radio Contact']
        dIN['Radio Contact'] = False
        del d
        return dIN


def drawStatusWindow():
    global yLine
    myscreen.addstr(yLine, 1, "##     Mission Time:     ##", curses.A_STANDOUT)
    yLine += 1
    myscreen.addstr(yLine, 4, str(round(fd['MET'], 1))
        .zfill(21), curses.color_pair(1))
    yLine += 1
    yLine += 1

    myscreen.addstr(yLine, 1, "ASL:")
    myscreen.addstr(yLine, 20, str(fd['ASL'])
        .zfill(filldigits))
    yLine += 1
    yLine += 1

    myscreen.addstr(yLine, 1, "##  Orbital Information  ##", curses.A_STANDOUT)
    yLine += 1
    myscreen.addstr(yLine, 1, "Apoapsis:")
    myscreen.addstr(yLine, 20, str(fd['Ap'])
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Periapsis:")
    myscreen.addstr(yLine, 20, str(fd['Pe'])
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Eccentricity:")
    myscreen.addstr(yLine, 20, str(round(fd['Eccentricity'], 6))
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Inclination:")
    myscreen.addstr(yLine, 20, str(round(fd['Inclination'], 6))
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Orbital Period:")
    myscreen.addstr(yLine, 20, str(round(fd['Orbital Period'], 1))
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Time to Ap:")
    myscreen.addstr(yLine, 20, str(round(fd['Time to Ap'], 1))
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Time to Pe:")
    myscreen.addstr(yLine, 20, str(round(fd['Time to Pe'], 1))
        .zfill(filldigits))
    yLine += 1
    yLine += 1

    myscreen.addstr(yLine, 1, "##  Flight Configuration  ##",
         curses.A_STANDOUT)
    yLine += 1
    myscreen.addstr(yLine, 1, "SAS Status:")
    myscreen.addstr(yLine, 20, str(fd['SAS Status']))
    yLine += 1
    myscreen.addstr(yLine, 1, "RCS Status:")
    myscreen.addstr(yLine, 20, str(fd['RCS Status']))
    yLine += 1
    myscreen.addstr(yLine, 1, "Ext. Light Status:")
    myscreen.addstr(yLine, 20, str(fd['Light Status']))
    yLine += 1
    yLine += 1

    myscreen.addstr(yLine, 1, "##       Resources        ##",
        curses.A_STANDOUT)
    yLine += 1
    myscreen.addstr(yLine, 1, "Electric Charge:")
    myscreen.addstr(yLine, 20, str(int(fd['ElectricCharge']))
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Liquid Fuel:")
    myscreen.addstr(yLine, 20, str(int(fd['LiquidFuel']))
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Oxidizer:")
    myscreen.addstr(yLine, 20, str(int(fd['Oxidizer']))
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Solid Fuel:")
    cSolidFuel = int(fd['SolidFuel'])
    if cSolidFuel < 0:
        myscreen.addstr(yLine, 20, "# None #", curses.color_pair(3))
    else:
        myscreen.addstr(yLine, 20, str(cSolidFuel).zfill(filldigits))
    yLine += 1
    yLine += 1


def formatRCC(inputln):  # Formating Reading Color Critical
    if int(inputln) < 0:
        inputln = str(int(inputln)).zfill(filldigits)
        return inputln, curses.color_pair(2)
    else:
        return str(int(inputln)).zfill(filldigits)


def drawVGauge(gLabel, percentVal, yCord, xCord):
    # Draws a gauge from 0-100% that is 30 rows x 15 Coll with the top left
    # corner at (yCord, xCord)
    percentVal = round(percentVal, 1)
    if percentVal > 100:
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
    elif percentVal < 1:
        gauge.addstr(23, 5, 'Empty')


###  Arduino Utilities



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

# Flight Data Memory and other variables
fd = {  # Primary data storage
'MET': -1, 'ASL': -1, 'Ap': -1, 'Pe': -1, 'Time to Ap': -1, 'Time to Pe': -1,
'Eccentricity': -1, 'Inclination': -1, 'Orbital Period': -1,
'Vertical Speed': -1, 'SAS Status': -1, 'RCS Status': -1, 'Light Status': -1,
'ElectricCharge': -1, 'Max ElectricCharge': -1, 'LiquidFuel': -1,
'Max LiquidFuel': -1, 'Oxidizer': -1, 'MaxOxidizer': -1, 'SolidFuel': -1,
'Max SolidFuel': -1, 'Radio Contact': False, 'Previous Radio Contact': False}
















arduinoSleepMarker = 0
buttonSleepMarker = 0
gearStatus = 0
brakeStatus = 0
memB = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Current serial input
memBOLD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Old serial input
n = 0
maxY, maxX = myscreen.getmaxyx()

### Flight Computer Section ##################################################
while chrin != 48:
    loopStartTime = time.time()
    if (maxY, maxX) != myscreen.getmaxyx():
        myscreen.clear()
    fd = getFlightData(fd)
    myscreen.border()
    maxY, maxX = myscreen.getmaxyx()
    yLine = 2  # Starting Row for flight info
    myscreen.nodelay(1)
    myscreen.addstr(0, maxX / 2 - 12, "Persigehl Flight Terminal")
    #

    #if fd['Radio Contact'] is True:
    if fd['Radio Contact'] is True and fd['Previous Radio Contact'] is True:
        drawStatusWindow()
    elif fd['Radio Contact'] is False:
        myscreen.addstr(max(yLine, 27), maxX / 2 - 12,
            "### Radio Contact Lost ###", curses.A_STANDOUT)
    elif fd['Radio Contact'] is True and fd['Previous Radio Contact'] is False:
        myscreen.clear()
        myscreen.border()
        drawStatusWindow()

    #myscreen.vline(20, 35, curses.ACS_CKBOARD, 4)
    #drawVGauge("Test Gauge", 42, 1, 35)
    drawVGauge("Electricity", fd['ElectricCharge'] /
        fd['Max ElectricCharge'] * 100, 1, 35)
    drawVGauge("Liquid Fuel", (fd['LiquidFuel'] /
        fd['Max LiquidFuel']) * 100, 1, 50)

    if fd['SolidFuel'] != -1:
        drawVGauge("Solid Fuel", (fd['SolidFuel'] /
            fd['Max SolidFuel']) * 100, 1, 65)
    else:
        drawVGauge("Solid Fuel", 0, 1, 65)

### Arduino Section ##########################################################
    if arduinoConnected is True:
        if chrin == 49:  # If user presses '1', toggle arduino bit
            if arduinoActive == 0:
                arduinoActive = 1
            elif arduinoActive == 1:
                arduinoActive = 0

        if arduinoActive == 0:
            myscreen.addstr(maxY - 1, 2, " Press 1 to Activate Arduino ")
        elif arduinoActive == 1:
            myscreen.addstr(maxY - 1, 2, " Press 1 to Deactivate Arduino ")
    else:
        myscreen.addstr(maxY - 1, 2, " Arduino not available ")


    if arduinoActive == 1:
        climbgauge = int(fd['Vertical Speed'])
        if climbgauge > 0:
            climbgauge = clamp((int(4 * math.sqrt(climbgauge)) + 127), 0, 254)
        elif climbgauge < 0:
            climbgauge = clamp((0 - int(4 * math.sqrt(
                abs(climbgauge))) + 127), 0, 254)
        else:
            climbgauge = 127  # Neutral

        memA = (str(int(round(fd["MET"]))).zfill(8)
            + str(int(round(fd["ASL"] / 100))).zfill(8)
            + str(int(round(fd["Ap"] / 100))).zfill(8)
            + str(int(round(fd["Pe"] / 100))).zfill(8)
            + str(int(round(fd['Vertical Speed']))).zfill(8)
            + chr(climbgauge) + 'BCDEFGH'
            )

        if arduinoSleepMarker > 0.2:
            try:
                push_to_arduino(memA)
            finally:
                arduinoSleepMarker = 0

        if ser.inWaiting > 9:
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

        if buttonSleepMarker > 0.1:
            buttonHandler()  # Reads memB for which buttons are pressed, then sends
                             # calls to telemachus as needed.
            button_sleep_marker = 0
            memBOLD = list(memB)

        myscreen.addstr(yLine, 1, "##   Arduino Readouts    ##",
         curses.A_STANDOUT)
        yLine += 1
        myscreen.addstr(yLine, 1, "memA:")
        myscreen.addstr(yLine, 20, str(memA))
        yLine += 1
        myscreen.addstr(yLine, 1, "memB:")
        myscreen.addstr(yLine, 20, str(memB))
        yLine += 1
        myscreen.addstr(yLine, 1, "Program Loop Time:")
        myscreen.addstr(yLine, 20, str(round(loopTime, 5)))
        yLine += 1
        yLine += 1








### Main Loop Cleanup ########################################################
    myscreen.addstr(maxY - 1, maxX - 19, " Press 0 to Exit ")
    myscreen.refresh()
    chrin = myscreen.getch()

    loopTimeOffset = 0.25 + loopStartTime - time.time()
    if loopTimeOffset > 0:
        time.sleep(loopTimeOffset)
    # Combined Bandwidth used based on interval:
    # 33ms = around 395 Packets/S, 345kbs
    # 25ms = around 500 Packets/S, 410kbs
    loopEndTime = time.time()
    loopTime = loopEndTime - loopStartTime
    arduinoSleepMarker += loopTime
    buttonSleepMarker += loopTime


curses.nocbreak()
myscreen.keypad(0)
curses.echo()
curses.endwin()
