from obd_capture import OBD_Capture

cap = OBD_Capture()
cap.connect()
obddata = cap.capture_data()
print(obddata)
