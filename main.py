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
from kivy.storage.jsonstore import JsonStore


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
        store = JsonStore('nebula_gui.json')
        if store.exists('executable_path'):
            self.executablePath = store.get('executable_path')['name']
        if 'config_path' in store:
            self.configPath = store['config_path']['name']

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
            store = JsonStore('nebula_gui.json')
            store.put('executable_path', name= paths[0])
            self.executablePath = store['executable_path']['name']

    def chooseConfig(self):
        paths = filechooser.open_file(title="Choose Nebula Config")
        
        if len(paths) > 0:
            store = JsonStore('nebula_gui.json')
            store.put('config_path', name= paths[0])
            self.configPath = store['config_path']['name']

class NebulaGUIApp(App):
    def build(self):
        return NebulaGUI()


if __name__ == '__main__':
    NebulaGUIApp().run()