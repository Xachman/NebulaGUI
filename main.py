from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.window import Window
from windows import windowsStartup
from nebula import runNebula
import threading
import os
from plyer import filechooser
from storage import Storage

store = Storage()

if os.name == 'nt':
    windowsStartup()

class NebulaGUI(BoxLayout):
    state = StringProperty("off")
    logs = StringProperty()
    executablePath = StringProperty("No Executable Selected")
    configPath = StringProperty("No Config Selected")
    the_popup = ObjectProperty(None)
    thread = None
    shouldDisconnect = False
    config = StringProperty()

    def __init__(self, *args, **kwargs):
        super(NebulaGUI, self).__init__(*args, **kwargs)
        if store.exists('executable_path'):
            self.executablePath = store.get('executable_path')
        if store.exists('config_path'):
            self.configPath = store.get('config_path')

    def changeState(self, state):
        self.state = state 

    def connect(self):
        if self.state == "off":
            self.changeState("on") 
            print(self.state)
            self.thread = threading.Thread(target=runNebula, args=("nebula", self.log, self.executablePath, self.configPath))
            self.thread.daemon = True
            self.thread.start()

    def disconnect(self):
        pass

    def log(self, line):
        if line.decode('utf-8') != "":
            print(line.decode('utf-8'))


    def chooseExecutable(self):
        paths = filechooser.open_file(title="Choose Nebula Executable")

        if len(paths) > 0:
            store.add('executable_path', paths[0])
            self.executablePath = store.get('executable_path')

    def chooseConfig(self):
        paths = filechooser.open_file(title="Choose Nebula Config")
        
        if len(paths) > 0:
            store.add('config_path', paths[0])
            self.configPath = store.get('config_path')

class NebulaGUIApp(App):
    def build(self):
        return NebulaGUI()


if __name__ == '__main__':
    NebulaGUIApp().run()