#!/usr/bin/env python
#Config File for JSON Proccessor and the python/telemachus library

def url():
    #return url = 'http://127.0.0.1:8085/telemachus/datalink?alt='
    return 'http://192.168.1.16:8085/telemachus/datalink?alt='
    # This is the URL that Telemachus can be found at.
    # Adjust it based on your firewall settings.


def arduinoSerialPort():
    return '/dev/ttyACM0'

def pollInterval():
    # How often should the program poll the game for flight data?
    return 0.250

