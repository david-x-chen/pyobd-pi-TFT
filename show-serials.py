from obd_capture import OBD_Capture

OBD_Capture.connect()
obddata = OBD_Capture.capture_data
print(obddata)
