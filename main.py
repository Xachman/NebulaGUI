
from windows import is_admin
from nebula import runNebula
import threading
import os
from storage import Storage
import pystray
from PIL import Image, ImageDraw
from pystray import Menu, MenuItem
from settings import SettingsApp

store = Storage()
thread = None
logStr = ''

def create_image(color=250):
    # Generate an image and draw a pattern
    width=16
    height=16
    color1=20
    color2=color
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

def setup(icon):
    icon.visible = True
def log(line):
    global logStr
    if line.decode('utf-8') != '':
        logStr=logStr+line.decode('utf-8')
        print(line.decode('utf-8'))
def connect(icon, item):
    global thread
    if thread is None:
        thread = threading.Thread(target=runNebula, args=("nebula", log, store.get('executable_path'), store.get('config_path')))
        thread.daemon = True
        thread.start()
        icon.icon = create_image((51,255,51))
def settings(icon, item):
    SettingsApp().run()
def quit(icon, item):
    icon.stop()
def menu():
    return Menu(
    MenuItem(
        'Connect',
        connect),
    MenuItem(
        'Settings',
        settings),
    MenuItem(
        'Quit',
        quit)
        )

if __name__ == '__main__':
    icon = pystray.Icon('test name', create_image(), menu=menu())
    #create_image().show()
    icon.run(setup)