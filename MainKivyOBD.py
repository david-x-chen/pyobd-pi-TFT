from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from kivy.uix.gridlayout import GridLayout
import threading
import time

from obd_connection import OBDConnection

Builder.load_file("MainKivyOBD.kv")

class OBDWidget(GridLayout):

    # Connection
    connection = None

    # Sensors
    sensors = []

    # Port
    port = None

    # List to hold children widgets
    boxes = []
    texts = []

    stop = threading.Event()

    def start_obd_connection(self):
        threading.Thread(target=self.obd_connection).start()

    def obd_connection(self):
        # Remove a widget, update a widget property, create a new widget,
        # add it and animate it in the main thread by scheduling a function
        # call with Clock.
        Clock.schedule_once(self.connecting, 0)

        # Do some thread blocking operations.
        time.sleep(1)

        # Update a widget property in the main thread by decorating the
        # called function with @mainthread.
        #self.update_status(l_text)

        # Remove some widgets and update some properties in the main thread
        # by decorating the called function with @mainthread.
        self.clean_up()

        # Start a new thread with an infinite loop and stop the current one.
        threading.Thread(target=self.start_connection).start()

    def connecting(self, *args):

        # Update a widget property.
        self.lab_rpm_name.text = 'Connecting to ELM device...'

        # Create and add a new widget.
        anim_bar = Factory.AnimWidget()
        self.anim_box.add_widget(anim_bar)

        # Animate the added widget.
        anim = Animation(opacity=0.3, width=100, duration=0.6)
        anim += Animation(opacity=1, width=400, duration=0.8)
        anim.repeat = True
        anim.start(anim_bar)

    @mainthread
    def update_status(self, new_text):
        self.status_lbl.text = new_text

    @mainthread
    def clean_up(self):
        self.lab_rpm_name.text = ''
        self.lab_rpm_value.text = ''
        self.remove_widget(self.anim_box)
        self.remove_widget(self.status_lbl.text)

    def connect(self, event):
        self.update_status("connecting...")

        self.update_status(" Opening interface (serial port)\n")
        self.update_status(" Trying to connect...\n")

        # Connection
        self.connection = OBDConnection()
        self.connection.connect()
        connected = False

        while not connected:
            connected = self.connection.is_connected()
            self.update_status("")
            self.update_status(" Trying to connect ..." + time.asctime())
            if connected:
                break

        if not connected:
            self.update_status(" Not connected\n")
            port_name = self.connection.get_port_name()
            if port_name:
                self.update_status(" Failed Connection: " + port_name +"\n")
                self.update_status(" Please hold alt & esc to view terminal.")
            return False
        else:
            self.update_status("")
            self.update_status(str(self.connection.get_output()))
            self.sensors = self.connection.get_sensors()
            self.port = self.connection.get_port()

    def refresh(self, event):
    	while True:
    	    time.sleep(1)
            self.displaySensorInfo()

    def start_connection(self):

        self.connect(None)
        self.update_status("")

        self.displaySensorInfo()

        time.sleep(1)
	    threading.Thread(target=self.refresh, args=(None,)).start()

    def getSensorsToDisplay(self, istart):
        sensors_display = []
        if istart < len(self.sensors):
            iend = istart + 1
            sensors_display = self.sensors[istart:iend]
        return sensors_display

    def displaySensorInfo(self):
        istart = 10 #speed
        sensors = self.getSensorsToDisplay(self.istart)

        sensorInfo(sensors, self.lab_rpm_name, self.lab_rpm_value)

        istart = 11 #rpm
        sensors = self.getSensorsToDisplay(self.istart)

        sensorInfo(sensors, self.lab_rpm_name, self.lab_rpm_value)

    def sensorInfo(self, sensors, nameLabel, valueLabel):
        print(sensors)
        # Create a box for each sensor
        for index, sensor in sensors:

            (name, value, unit) = self.port.sensor(index)

            # Text for sensor value
            if type(value)==float:
                value = str("%.2f"%round(value, 3))

            valueLabel.text = str(value)
            # Text for sensor name
            nameLabel.text = name + " " + unit

            print(name + ": " + str(value) + " " + unit)

class ThreadedApp(App):

    def on_start(self):
        self.root.start_obd_connection()

    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        self.root.stop.set()

    def build(self):
        return OBDWidget()

if __name__ == '__main__':
    ThreadedApp().run()
