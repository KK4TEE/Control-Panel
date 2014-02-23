# python 2.7


import math
import time
import curses
import telemachus_plugin as tele


def formatReading(inputln):
    return str(int(inputln)).zfill(filldigits)


myscreen = curses.initscr()
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
        .zfill(21))
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

    myscreen.addstr(yLine, 1, "##  Flight Configuration  ##", curses.A_STANDOUT)
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

    myscreen.addstr(yLine, 1, "##       Resources        ##", curses.A_STANDOUT)
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
    myscreen.addstr(yLine, 20, str(int(tele.read_resource('SolidFuel'))
        ).zfill(filldigits))
    yLine += 1
    yLine += 1
    myscreen.addstr(yLine, 1, "Press 0 to exit")

    myscreen.refresh()
    chrin = myscreen.getch()

    time.sleep(0.25)


curses.nocbreak()
myscreen.keypad(0)
curses.echo()
curses.endwin()
