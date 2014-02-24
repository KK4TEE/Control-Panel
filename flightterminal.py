# python 2.7

# note: The data gathering portion of this should be centralized
# At the begining of each loop all needed data should be collected
# and then referenced as a local variable. I'll rewrite this when I
# get the chance.
import math
import time
import curses
import telemachus_plugin as tele


def getFlightData(d):
    d['MET'] = int(tele.read_missiontime())
    d['ASL'] = int(tele.read_asl())
    d['Ap'] = int(tele.read_apoapsis())
    d['Pe'] = int(tele.read_periapsis())
    d['Time to Ap'] = float(tele.read_time_to_ap())
    d['Time to Pe'] = float(tele.read_time_to_pe())
    d['Eccentricity'] = float(tele.read_eccentricity())
    d['Inclination'] = float(tele.read_inclination())
    d['Orbital Period'] = float(tele.read_orbitalperiod())

    d['SAS Status'] = int(tele.sas(2))
    d['RCS Status'] = int(tele.rcs(2))
    d['Light Status'] = int(tele.light(2))

    d['ElectricCharge'] = float(tele.read_resource('ElectricCharge'))
    d['Max ElectricCharge'] = float(tele.read_resource_max('ElectricCharge'))
    d['LiquidFuel'] = float(tele.read_resource('LiquidFuel'))
    d['Max LiquidFuel'] = float(tele.read_resource_max('LiquidFuel'))
    d['Oxidizer'] = float(tele.read_resource('Oxidizer'))
    d['MaxOxidizer'] = float(tele.read_resource_max('Oxidizer'))
    d['SolidFuel'] = float(tele.read_resource('SolidFuel'))
    d['Max SolidFuel'] = float(tele.read_resource_max('SolidFuel'))

    return d


def formatRCC(inputln):  # Formating Reading Color Critical
    if int(inputln) < 0:
        inputln = str(int(inputln)).zfill(filldigits)
        return inputln, curses.color_pair(2)
    else:
        return str(int(inputln)).zfill(filldigits)


def drawVGauge(gLabel, percentVal, yCord, xCord):
    # Draws a gauge from 0-100% that is 30 rows x 15 Coll with the top left
    # corner at (yCord, xCord)
    percentVal = round(percentVal,1)
    if percentVal > 100:
        percentVal == int(100)
    gauge = myscreen.subwin(25, 15, yCord, xCord)
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
    elif percentVal < 0.1:
        gauge.addstr(23, 6, 'Empty')


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

# Flight Data Memory
fd = {'zero': 0}

while chrin != 48:
    fd = getFlightData(fd)
    myscreen.border()
    maxY, maxX = myscreen.getmaxyx()
    yLine = 2  # Starting Row for flight info
    myscreen.nodelay(1)
    myscreen.addstr(0, maxX / 2 - 12, "Persigehl Flight Terminal")
    #
    myscreen.addstr(yLine, 1, "##     Mission Time:     ##", curses.A_STANDOUT)
    yLine += 1
    myscreen.addstr(yLine, 4, str(fd['MET'])
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
        myscreen.addstr(yLine, 19, "# Empty #", curses.color_pair(3))
    else:
        myscreen.addstr(yLine, 20, str(cSolidFuel).zfill(filldigits))
    yLine += 1
    yLine += 1

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

    if chrin == 49:  # If user presses '1', toggle arduino bit
        if arduinoActive == 0:
            arduinoActive = 1
        elif arduinoActive == 1:
            arduinoActive = 0

    if arduinoActive == 0:
        myscreen.addstr(maxY - 1, 2, " Press 1 to Activate Arduino ")
    elif arduinoActive == 1:
        myscreen.addstr(maxY - 1, 2, " Press 1 to DeActivate Arduino ")

    myscreen.addstr(maxY - 1, maxX - 19, " Press 0 to Exit ")
    myscreen.refresh()
    chrin = myscreen.getch()
    time.sleep(0.25)


curses.nocbreak()
myscreen.keypad(0)
curses.echo()
curses.endwin()
