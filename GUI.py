import kivy # importing main package

from kivy.app import App  # required base class for your app
from kivy.uix.label import Label  # uix element that will hold text
from kivy.uix.gridlayout import GridLayout  # one of many layout structures
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.textinput import TextInput  # allow for ...text input.
from kivy.uix.button import Button
from kivy.lang import Builder

kivy.require('1.11.1')

program_version = "0.0."
program_name = "balance calculator"
program_date = "2019"

class Infoscreen(GridLayout):
    def __init__(self, **kwargs):
        # we want to run __init__ of both ConnectPage AAAAND GridLayout
        super().__init__(**kwargs)
        global program_version
        global program_name
        global program_date
        print()
        self.cols = 1  # used for our grid
        self.add_widget(Label(text= "[size=40][color=3333ff]" + program_name.upper() + "[/color][/size]", markup=True))
        self.add_widget(Label(text ="version: " + program_version))
        self.add_widget(Label(text=""))
        self.add_widget(Label(text=program_date))

        Clock.schedule_once(self.enter_mainscreen, 3)

    def enter_mainscreen(self, _):
        bilance_calculator.screen_manager.current = 'Main'


class Mainscreen(GridLayout):
    def __init__(self, **kwargs):
        # we want to run __init__ of both ConnectPage AAAAND GridLayout
        super().__init__(**kwargs)


class main_app(App):
    def build(self):
        # We are going to use screen manager, so we can add multiple screens
        self.screen_manager = ScreenManager()

        #Adding info screen to meneger
        self.info_screen = Infoscreen()
        screen = Screen(name='Info')
        screen.add_widget(self.info_screen)
        self.screen_manager.add_widget(screen)

        # Adding main screen to meneger
        self.main_screen = Mainscreen()
        screen = Screen(name='Main')
        screen.add_widget(self.main_screen)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


# Run the app.
if __name__ == "__main__":
    bilance_calculator = main_app()
    bilance_calculator.run()