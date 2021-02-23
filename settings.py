from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from storage import Storage
from plyer import filechooser

store = Storage()
class Settings(BoxLayout):
    state = StringProperty("off")
    executablePath = StringProperty("No Executable Selected")
    configPath = StringProperty("No Config Selected")
    config = StringProperty()

    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)
        if store.exists('executable_path'):
            self.executablePath = store.get('executable_path')
        if store.exists('config_path'):
            self.configPath = store.get('config_path')

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

class SettingsApp(App):
    def build(self):
        from kivy.core.window import Window
        Window.bind(on_request_close=self.on_request_close)
        return Settings()
    def on_request_close(self, *args):
        from kivy.core.window import Window
        Window.hide()