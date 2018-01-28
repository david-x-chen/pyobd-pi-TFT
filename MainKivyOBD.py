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

    stop = threading.Event()

    def start_obd_connection(self):
        threading.Thread(target=self.obd_connection).start()

    def obd_connection(self):
        # Remove a widget, update a widget property, create a new widget,
        # add it and animate it in the main thread by scheduling a function
        # call with Clock.
        Clock.schedule_once(self.start_connection, 0)

        # Do some thread blocking operations.
        time.sleep(5)

        # Update a widget property in the main thread by decorating the
        # called function with @mainthread.
        #self.update_status(l_text)

        # Remove some widgets and update some properties in the main thread
        # by decorating the called function with @mainthread.
        self.clean_up()

        # Start a new thread with an infinite loop and stop the current one.
        threading.Thread(target=self.showSensors).start()

    def start_connection(self, *args):

        # Update a widget property.
        self.lab_1.text = 'Connecting to ELM device...'

        self.connect(None)

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
        self.lab_1.text = ''
        self.lab_2.text = ''
        self.remove_widget(self.anim_box)

    def connect(self, event):
        self.update_status("connecting...")

        # Connection
        self.c = None

        # Connection
        self.connection = None

        # Sensors
        self.istart = 0
        self.sensors = []

        # Port
        self.port = None

        # List to hold children widgets
        self.boxes = []
        self.texts = []

        self.update_status(" Opening interface (serial port)\n")
        self.update_status(" Trying to connect...\n")

        # Connection
        self.c = OBDConnection()
        self.c.connect()
        connected = False

        failedCount = 0
        while not connected:
            connected = self.c.is_connected()
            self.update_status("")
            self.update_status(" Trying to connect ..." + time.asctime())
            if connected:
                break

            if failedCount > 5:
                self.stop.set()
                break

            failedCount += 1

        if not connected:
            self.update_status(" Not connected\n")
            return False
        else:
            self.update_status("")
            port_name = self.c.get_port_name()
            if port_name:
                self.update_status(" Failed Connection: " + port_name +"\n")
                self.update_status(" Please hold alt & esc to view terminal.")
            self.update_status(str(self.c.get_output()))
            self.sensors = self.c.get_sensors()
            self.port = self.c.get_port()

    def setConnection(self, connection):
        self.connection = connection

    def setSensors(self, sensors):
        self.sensors = sensors

    def setPort(self, port):
        self.port = port

    def getSensorsToDisplay(self, istart):
        sensors_display = []
        if istart<len(self.sensors):
            iend = istart + 1
            sensors_display = self.sensors[istart:iend]
        return sensors_display

    def refresh(self, event):
        sensors = self.getSensorsToDisplay(self.istart)

        itext = 0
        for index, sensor in sensors:

            (name, value, unit) = self.port.sensor(index)
            if type(value)==float:
                value = str("%.2f"%round(value, 3))

            if itext<len(self.texts):
                self.texts[itext*2].SetLabel(str(value))

            itext += 1

    def showSensors(self):

        sensors = self.getSensorsToDisplay(self.istart)

        # Create a box for each sensor
        for index, sensor in sensors:

            (name, value, unit) = self.port.sensor(index)

            # Text for sensor value
            if type(value)==float:
                value = str("%.2f"%round(value, 3))

            self.lab_2.text = value

            print(value)

            # Text for sensor name
            self.lab_1.text = name + " " + unit

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
