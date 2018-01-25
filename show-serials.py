from obd_capture import OBD_Capture

cap = OBD_Capture()
obddata = cap.capture_data
print(obddata)
