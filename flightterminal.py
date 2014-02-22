# python 2.7


import math
import time
import curses
import telemachus_plugin as tele

myscreen = curses.initscr()
curses.noecho()
curses.cbreak()

myscreen.border()
myscreen.keypad(1)

chrin = -1

while chrin != 48:
    yLine = 2 # Starting Row for flight info
    myscreen.nodelay(1)
    myscreen.addstr(0, 25, "Persigehl Flight Terminal")
    #
    myscreen.addstr(yLine, 1, "Mission Time:")
    myscreen.addstr(yLine, 20, str(int(tele.read_missiontime())))
    yLine += 1
    yLine += 1

    myscreen.addstr(yLine, 1, "ASL:")
    myscreen.addstr(yLine, 20, str(int(tele.read_asl())))
    yLine += 1
    yLine += 1

    myscreen.addstr(yLine, 1, "## Orbital Information ##")
    yLine += 1
    myscreen.addstr(yLine, 1, "Apoapsis:")
    myscreen.addstr(yLine, 20, str(int(tele.read_apoapsis())))
    yLine += 1
    myscreen.addstr(yLine, 1, "Periapsis:")
    myscreen.addstr(yLine, 20, str(int(tele.read_periapsis())))
    yLine += 1
    myscreen.addstr(yLine, 1, "Eccentricity:")
    myscreen.addstr(yLine, 20, str(round(tele.read_eccentricity(), 6)))
    yLine += 1
    myscreen.addstr(yLine, 1, "Inclination:")
    myscreen.addstr(yLine, 20, str(round(tele.read_inclination(), 6)))
    yLine += 1
    myscreen.addstr(yLine, 1, "Orbital Period:")
    myscreen.addstr(yLine, 20, str(round(tele.read_orbitalperiod(), 1)))
    yLine += 1
    myscreen.addstr(yLine, 1, "Time to Ap:")
    myscreen.addstr(yLine, 20, str(round(tele.read_time_to_ap(), 1)))
    yLine += 1
    myscreen.addstr(yLine, 1, "Time to Pe:")
    myscreen.addstr(yLine, 20, str(round(tele.read_time_to_pe(), 1)))
    yLine += 1
    yLine += 1

    myscreen.addstr(yLine, 1, "## Flight Configuration ##")
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

    myscreen.addstr(yLine, 1, "## Resources ##")
    yLine += 1
    myscreen.addstr(yLine, 1, "Electric Charge:")
    myscreen.addstr(yLine, 20, str(int(tele.read_resource('ElectricCharge'))))
    yLine += 1
    myscreen.addstr(yLine, 1, "Liquid Fuel:")
    myscreen.addstr(yLine, 20, str(int(tele.read_resource('LiquidFuel'))))
    yLine += 1
    myscreen.addstr(yLine, 1, "Oxidizer:")
    myscreen.addstr(yLine, 20, str(int(tele.read_resource('Oxidizer'))))
    yLine += 1
    myscreen.addstr(yLine, 1, "Solid Fuel:")
    myscreen.addstr(yLine, 20, str(int(tele.read_resource('SolidFuel'))))
    yLine += 1
    yLine += 1
    myscreen.addstr(yLine, 1, "Press 0 to exit")

    myscreen.refresh()
    chrin = myscreen.getch()

    time.sleep(0.1)


curses.nocbreak()
myscreen.keypad(0)
curses.echo()
curses.endwin()
