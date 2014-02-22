#Config File for JSON Proccessor and the python/telemachus library
import serial

url = 'http://127.0.0.1:8085/telemachus/datalink?alt='
#url = 'http://192.168.1.3:8085/telemachus/datalink?alt='
    # This is the URL that Telemachus can be found at.
    # Adjust it based on your firewall settings.


ser = serial.Serial(
    port='/dev/ttyACM0',
    #port='COM3',
    #baudrate=115200, # Causes the arduino buffer to fill up
    baudrate=9600, # Seems to be working well
   # parity=serial.PARITY_ODD,
   # stopbits=serial.STOPBITS_TWO,
   # bytesize=serial.SEVENBITS
)
