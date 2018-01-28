from obd_connection import OBDConnection
import obd_sensors

#connection = OBDConnection()
#connection.connect()
#connected = False
#sensors = []
#port = ""

#while not connected:
#connected = connection.is_connected()
#    if connected:
#        break

#if not connected:
#    port_name = connection.get_port_name()
#    if port_name:
#        print(" Failed Connection: " + port_name +"\n")
#        print(" Please hold alt & esc to view terminal.")
#else:
#    print("")
#    print(str(connection.get_output()))
#    sensors = connection.get_sensors()
#    port = connection.get_port()

sensors = []
for index in xrange(len(obd_sensors.SENSORS)):
    sensor = obd_sensors.SENSORS[index]
    sensors.append(sensor)
    #print(sensor.shortname)
    #print(obd_sensors.SENSORS[index])
rpm = filter(lambda sensor: sensor.shortname == 'rpm', obd_sensors.SENSORS)[0]
print(rpm.shortname)

#for index, sensor in sensors:

#    (name, value, unit) = port.sensor(index)

    # Text for sensor value
#    if type(value)==float:
#        value = str("%.2f"%round(value, 3))

#    print(name + ": " + str(value) + " " + unit)

#print(sensors)
