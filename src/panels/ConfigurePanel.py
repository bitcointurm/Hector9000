import sys
import time
import json
from kivy.core.text import Label
from kivy.properties import ListProperty, BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from hardware.HectorConfig import config
from hardware.HectorHardware import HectorHardware


class ConfigurePanel(Screen):

    def exit(self):
        print("exit")
        root = BoxLayout(orientation='vertical')
        root2 = BoxLayout()
        root2.add_widget(
            Label(text='Do you realy want to close satoshi 24 ? \nThere will be no more drinks ....', font_size='35sp'))
        root.add_widget(root2)

        root3 = BoxLayout(size_hint_y=0.15)
        buttOK = Button(text='OK', font_size=60)
        root3.add_widget(buttOK)

        buttCancel = Button(text='Cancel', font_size=60)
        root3.add_widget(buttCancel)
        root.add_widget(root3)

        popup = Popup(title='WAIT !!!', content=root,
                      auto_dismiss=False)

        buttOK.bind(on_press=self.shutdown)
        buttCancel.bind(on_press=popup.dismiss)
        #popup.bind(on_dismiss=self.shutdown)
        popup.open()

    def shutdown(self, instance):
        hector = HectorHardware(config)
        hector.cleanAndExit()
        sys.exit()

    pass
