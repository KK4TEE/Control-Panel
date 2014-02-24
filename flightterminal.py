# python 2.7

# note: The data gathering portion of this should be centralized
# At the begining of each loop all needed data should be collected
# and then referenced as a local variable. I'll rewrite this when I
# get the chance.
import math
import time
import curses
import telemachus_plugin as tele


def formatRCC(inputln):  # Formating Reading Color Critical
    if int(inputln) < 0:
        inputln = str(int(inputln)).zfill(filldigits)
        return inputln, curses.color_pair(2)
    else:
        return str(int(inputln)).zfill(filldigits)


def drawVGauge(gLabel, percentVal, yCord, xCord):
    # Draws a gauge from 0-100% that is 30 rows x 15 Coll with the top left
    # corner at (yCord, xCord)
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
        gauge.addstr(23, 6, str(percentVal).zfill(3) + '%')
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

while chrin != 48:
    myscreen.border()
    maxY, maxX = myscreen.getmaxyx()
    yLine = 2  # Starting Row for flight info
    myscreen.nodelay(1)
    myscreen.addstr(0, maxX / 2 - 12, "Persigehl Flight Terminal")
    #
    myscreen.addstr(yLine, 1, "##     Mission Time:     ##", curses.A_STANDOUT)
    yLine += 1
    myscreen.addstr(yLine, 4, str(int(tele.read_missiontime()))
        .zfill(21), curses.color_pair(1))
    yLine += 1
    yLine += 1

    myscreen.addstr(yLine, 1, "ASL:")
    myscreen.addstr(yLine, 20, str(int(tele.read_asl()))
        .zfill(filldigits))
    yLine += 1
    yLine += 1

    myscreen.addstr(yLine, 1, "##  Orbital Information  ##", curses.A_STANDOUT)
    yLine += 1
    myscreen.addstr(yLine, 1, "Apoapsis:")
    myscreen.addstr(yLine, 20, str(int(tele.read_apoapsis()))
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Periapsis:")
    myscreen.addstr(yLine, 20, str(int(tele.read_periapsis()))
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Eccentricity:")
    myscreen.addstr(yLine, 20, str(round(tele.read_eccentricity(), 6))
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Inclination:")
    myscreen.addstr(yLine, 20, str(round(tele.read_inclination(), 6))
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Orbital Period:")
    myscreen.addstr(yLine, 20, str(round(tele.read_orbitalperiod(), 1))
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Time to Ap:")
    myscreen.addstr(yLine, 20, str(round(tele.read_time_to_ap(), 1))
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Time to Pe:")
    myscreen.addstr(yLine, 20, str(round(tele.read_time_to_pe(), 1))
        .zfill(filldigits))
    yLine += 1
    yLine += 1

    myscreen.addstr(yLine, 1, "##  Flight Configuration  ##",
         curses.A_STANDOUT)
    yLine += 1
    myscreen.addstr(yLine, 1, "SAS Status:")
    myscreen.addstr(yLine, 20, str((tele.sas(2))))
    yLine += 1
    myscreen.addstr(yLine, 1, "RCS Status:")
    myscreen.addstr(yLine, 20, str((tele.rcs(2))))
    yLine += 1
    myscreen.addstr(yLine, 1, "Ext. Light Status:")
    myscreen.addstr(yLine, 20, str((tele.light(2))))
    yLine += 1
    yLine += 1

    myscreen.addstr(yLine, 1, "##       Resources        ##",
        curses.A_STANDOUT)
    yLine += 1
    myscreen.addstr(yLine, 1, "Electric Charge:")
    myscreen.addstr(yLine, 20, str(int(tele.read_resource('ElectricCharge')))
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Liquid Fuel:")
    myscreen.addstr(yLine, 20, str(int(tele.read_resource('LiquidFuel')))
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Oxidizer:")
    myscreen.addstr(yLine, 20, str(int(tele.read_resource('Oxidizer')))
        .zfill(filldigits))
    yLine += 1
    myscreen.addstr(yLine, 1, "Solid Fuel:")
    cSolidFuel = int(tele.read_resource('SolidFuel'))
    if cSolidFuel < 0:
        myscreen.addstr(yLine, 19, "# Empty #", curses.color_pair(3))
    else:
        myscreen.addstr(yLine, 20, str(cSolidFuel).zfill(filldigits))
    yLine += 1
    yLine += 1

    myscreen.addstr(maxY - 1, maxX - 19, " Press 0 to Exit ")

    #myscreen.vline(20, 35, curses.ACS_CKBOARD, 4)
    #drawVGauge("Test Gauge", 42, 1, 35)
    drawVGauge("Electricity", int(tele.read_resource('ElectricCharge') /
        int(tele.read_resource_max('ElectricCharge')) * 100), 1, 35)
    drawVGauge("Liquid Fuel", int(tele.read_resource('LiquidFuel') /
        int(tele.read_resource_max('LiquidFuel')) * 100), 1, 50)
    drawVGauge("Solid Fuel", int(tele.read_resource('SolidFuel') /
        (int(tele.read_resource_max('SolidFuel')) + 2) * 100), 1, 65)
        # The above will need to be updated with a proper handling of
        # Telemachus returning '-1' when there is none of a resource
        # on board.Adding to (so as to get -1 / 2) is a mere stop gap.
    myscreen.refresh()

    chrin = myscreen.getch()

    time.sleep(0.25)


curses.nocbreak()
myscreen.keypad(0)
curses.echo()
curses.endwin()
