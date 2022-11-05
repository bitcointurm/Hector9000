from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from panels.MainPanel import MainPanel
from panels.ConfigurePanel import ConfigurePanel
from panels.CleanerPanel import CleanerPanel

Config.set('graphics', 'fullscreen', 'auto') # 'auto' -> Fullscreen | '0' -> NormalMode


class MyScreenManager(ScreenManager):
    pass


myfile = open('window-image-conf', 'r')
root_widget = Builder.load_string(myfile.read())


class Panel(App):
    def build(self):
        return root_widget


if __name__ == "__main__":
    Panel().run()
