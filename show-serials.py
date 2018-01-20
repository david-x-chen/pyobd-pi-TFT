import serial
from obd_utils import serial

portnames = scanSerial()
print portnames
for port in portnames:
    print port
