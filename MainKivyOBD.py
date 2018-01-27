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

    def start_second_thread(self, l_text):
        threading.Thread(target=self.second_thread, args=(l_text,)).start()

    def second_thread(self, label_text):
        # Remove a widget, update a widget property, create a new widget,
        # add it and animate it in the main thread by scheduling a function
        # call with Clock.
        Clock.schedule_once(self.start_test, 0)

        # Do some thread blocking operations.
        time.sleep(5)
        l_text = str(int(label_text) * 3000)

        # Update a widget property in the main thread by decorating the
        # called function with @mainthread.
        self.update_label_text(l_text)

        # Do some more blocking operations.
        time.sleep(2)

        # Remove some widgets and update some properties in the main thread
        # by decorating the called function with @mainthread.
        self.stop_test()

        # Start a new thread with an infinite loop and stop the current one.
        threading.Thread(target=self.connect, args=(None,)).start()

    def start_test(self, *args):

        # Update a widget property.
        self.lab_1.text = ('The UI remains responsive while the '
                           'second thread is running.')

        # Create and add a new widget.
        anim_bar = Factory.AnimWidget()
        self.anim_box.add_widget(anim_bar)

        # Animate the added widget.
        anim = Animation(opacity=0.3, width=100, duration=0.6)
        anim += Animation(opacity=1, width=400, duration=0.8)
        anim.repeat = True
        anim.start(anim_bar)

    @mainthread
    def update_label_text(self, new_text):
        self.lab_2.text = new_text

    @mainthread
    def stop_test(self):
        self.lab_1.text = ('Second thread exited, a new thread has started. '
                           'Close the app to exit the new thread and stop '
                           'the main process.')

        self.lab_2.text = str(int(self.lab_2.text) + 1)

        self.remove_widget(self.anim_box)

    def connect(self, event):
        print("connecting...")

        # Connection
        self.c = None

        # Sensors list
        self.sensors = []

        # Port
        self.port = None

        self.status_lbl.text = " Opening interface (serial port)\n"
        self.status_lbl.text = " Trying to connect...\n"

        # Connection
        self.c = OBDConnection()
        self.c.connect()
        connected = False

        failedCount = 0
        while not connected:
            connected = self.c.is_connected()
            self.status_lbl.text = ""
            self.status_lbl.text = " Trying to connect ..." + time.asctime()
            if connected:
                break

            if failedCount > 5:
                self.root.stop.set()

            failedCount += 1

        if not connected:
            self.status_lbl.text = " Not connected\n"
            return False
        else:
            self.status_lbl.text = ""
            port_name = self.c.get_port_name()
            if port_name:
                self.status_lbl.text = " Failed Connection: " + port_name +"\n"
                self.status_lbl.text = " Please hold alt & esc to view terminal."
            self.status_lbl.text = str(self.c.get_output())
            self.sensors = self.c.get_sensors()
            self.port = self.c.get_port()


class ThreadedApp(App):

    def on_start(self):
        self.root.start_second_thread("3")

    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        self.root.stop.set()

    def build(self):
        return OBDWidget()

if __name__ == '__main__':
    ThreadedApp().run()
