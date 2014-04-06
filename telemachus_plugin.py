
# This allows you to more conveniently write scripts that can interface with
# Telemachus
#url = 'http://127.0.0.1:8085/telemachus/datalink?alt='
#url = 'http://192.168.1.3:8085/telemachus/datalink?alt='
    # This is the URL that Telemachus can be found at.
    # Adjust it based on your firewall settings.

import json
import urllib2
import time
import os
import math
import config

url = config.url()
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
        result = math.radians(int(fresh_json["alt"]))
    elif dimension in ['yaw']:
        fresh_json = json.load(urllib2.urlopen(url + 'n.heading'))
        result = math.radians(int(fresh_json["alt"]))
    elif dimension in ['roll']:
        fresh_json = json.load(urllib2.urlopen(url + 'n.roll'))
        result = math.radians(int(fresh_json["alt"]))
    else:
        result = -1
    return result


def read_heading():
    #Note: This returns facing:yaw, not your heading over land
    #Basically what the navball shows, not 'true' heading
    fresh_json = json.load(urllib2.urlopen(url + 'n.heading'))
    result = math.radians(int(fresh_json["alt"]))
    return result


def read_inclination():
    fresh_json = json.load(urllib2.urlopen(url + 'o.inclination'))
    result = math.radians(int(fresh_json["alt"]))
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

def read_time_to_ap():
    fresh_json = json.load(urllib2.urlopen(url + 'o.timeToAp'))
    result = fresh_json["alt"]
    return result

def read_time_to_pe():
    fresh_json = json.load(urllib2.urlopen(url + 'o.timeToPe'))
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

def read_heightFromTerrain():
    fresh_json = json.load(urllib2.urlopen(url + 'v.heightFromTerrain'))
    result = fresh_json["alt"]
    return result

# Output Definitions


def abort():
    urllib2.urlopen(url + 'f.abort')


def fly_by_wire(var):
    urllib2.urlopen(url + 'v.setFbW' + '[' + str(var) + ']')


def brake(var):
    if var == 2:
        #fresh_json = json.load(urllib2.urlopen(url + 'v.gearValue'))
        #return fresh_json["alt"]
        return (-1)
        #print 'The brake:read feature is not yet support by telemachus'
    elif var == 1:
        urllib2.urlopen(url + 'f.brake' + '[' + 'true' + ']')
        #print 'Setting Brake to on'
    elif var == 0:
        urllib2.urlopen(url + 'f.brake' + '[' + 'false' + ']')
        #print 'Setting Brake to off'
    else:
        return (-1)
        #print 'Brake value was set wrong'


def gear(var):
    if var == 2:
        #fresh_json = json.load(urllib2.urlopen(url + 'v.gearValue'))
        #return fresh_json["alt"]
        return (-1)
        #print 'The gear:read feature is not yet support by telemachus'
    elif var == 1:
        urllib2.urlopen(url + 'f.gear' + '[' + 'true' + ']')
        #print 'Setting Gear to on'
    elif var == 0:
        urllib2.urlopen(url + 'f.gear' + '[' + 'false' + ']')
        #print 'Setting Gear to off'
    else:
        return (-1)
        #print 'Gear value was set wrong'


def light(var):
    if var == 2:
        fresh_json = json.load(urllib2.urlopen(url + 'v.lightValue'))
        if fresh_json["alt"] == "True":
            return 1
        elif fresh_json["alt"] == "False":
            return 0
        else:
            return fresh_json["alt"]
    elif var == 1:
        urllib2.urlopen(url + 'f.light' + '[' + 'true' + ']')
        #print 'Setting Light to TRUE'
    elif var == 0:
        urllib2.urlopen(url + 'f.light' + '[' + 'false' + ']')
        #print 'Setting Light to False'
    else:
        return (-1)
        #print 'Light value was set wrong'


def rcs(var):
    if var == 2:
        fresh_json = json.load(urllib2.urlopen(url + 'v.rcsValue'))
        if fresh_json["alt"] == "True":
            return 1
        elif fresh_json["alt"] == "False":
            return 0
        else:
            return fresh_json["alt"]
    elif var == 1:
        urllib2.urlopen(url + 'f.rcs' + '[' + 'true' + ']')
        #print 'Setting RCS to TRUE'
    elif var == 0:
        urllib2.urlopen(url + 'f.rcs' + '[' + 'false' + ']')
        #print 'Setting RCS to False'
    else:
        return (-1)
        #print 'RCS value was set wrong'


def sas(var):
    if var == 2:
        fresh_json = json.load(urllib2.urlopen(url + 'v.sasValue'))
        if fresh_json["alt"] == "True":
            return 1
        elif fresh_json["alt"] == "False":
            return 0
        else:
            return fresh_json["alt"]
    elif var == 1:
        urllib2.urlopen(url + 'f.sas' + '[' + 'true' + ']')
        #print 'Setting SAS to TRUE'
    elif var == 0:
        urllib2.urlopen(url + 'f.sas' + '[' + 'false' + ']')
        #print 'Setting SAS to False'
    else:
        return (-1)
        #print 'SAS value was set wrong'


def stage():
    urllib2.urlopen(url + 'f.stage')


def set_facing(dimension, angle):
    #This is done by setting relative positions from 0 to 1, as a percent
    #This is based on the three bars in the lower left corner, NOT the Navball
    if dimension in ['pitch']:
        urllib2.urlopen(url + 'v.setPitch' + '[' + str(angle) + ']')

    elif dimension in ['yaw']:
        urllib2.urlopen(url + 'v.setYaw' + '[' + str(angle) + ']')

    elif dimension in ['roll']:
        urllib2.urlopen(url + 'v.setRoll' + '[' + str(angle) + ']')


def set_throttle(throttle):
    urllib2.urlopen(url + 'f.setThrottle' + '[' + str(throttle) + ']')


def toggle_ag(agn):
    urllib2.urlopen(url + 'f.ag' + agn)



