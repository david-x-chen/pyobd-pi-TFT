
from obd_capture import OBD_Capture
from threading import Thread

class OBDConnection(object):
    """
    Class for OBD connection. Use a thread for connection.
    """

    def __init__(self):
        self.c = OBD_Capture()

    def get_capture(self):
        return self.c

    def obd_connect(self, o):
        o.connect()

    def connect(self):
        self.t = Thread(target=self.obd_connect, args=(self.c,))
        self.t.start()

    def is_connected(self):
        return self.c.is_connected()

    def get_output(self):
        if self.c and self.c.is_connected():
            return self.c.capture_data()
        return ""

    def get_port(self):
        return self.c.is_connected()

    def get_port_name(self):
        if self.c:
            port = self.c.is_connected()
            if port:
                try:
                    return port.port.name
                except:
                    pass
        return None

    def get_sensors(self):
        sensors = []
        if self.c:
            sensors = self.c.getSupportedSensorList()
        return sensors
