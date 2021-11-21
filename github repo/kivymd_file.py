import kivy
from kivy.core.window import Window
import certifi as cfi

from kivy.lang import Builder, builder
from kivy.network.urlrequest import UrlRequest
try:
    from widgets import screen_helper

except:
    pass
from kivy.uix.screenmanager import Screen, ScreenManager

from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivymd.utils.fitimage import FitImage
from kivy.properties import (
    StringProperty,
    BooleanProperty,
    ObjectProperty,
    NumericProperty,
    ListProperty,
    OptionProperty,
)


class Studio(Screen):
    # this is a good idea, to implement it, you should add it using clock
    pass

sm = ScreenManager()
sm.add_widget(Studio(name='Studio'))

KV = '''
Screen:
    ScreenManager:
        id: manager #this is needed
        Screen:
            name : 'studio'
            MDFloatLayout:
                Image: #if we use FitImage: is not good, because FitImage does not update images, but Image does
                    id: cover_pic
                    orientation: "vertical"
                    source: "C:/Users/ghassen/Downloads/600-900.jpg"
                Image: #the FitImage: class does not update media, but Image does
                    id: profile_pic
                    size_hint: None, None
                    source: "Photos/pro.jpg"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    radius: 60, 60, 60, 60
                    #
                TooltipMDIconButton:  #kivy.factory.FactoryException: Unknown class <TooltipMDIconButton>
                    tooltip_text : 'Edit Profile Picture'
                    id: edit_profile_pic
                    icon: "image-edit-outline"
                    disabled: True
                    pos_hint: {'center_x':0.5,'center_y':0.5}
                    user_font_size: "25sp"
                    on_release: app.file_manager_open_for_profile()
                MDRaisedButton:
                    pos_hint: {'center_x':0.5, 'center_y':0.3}
                    text: 'Predict'
                    on_press: app.predict()
                MDLabel:
                    text: 'Plant disease predictor'
                    halign: 'center'
                    pos_hint: {'center_y':0.9}
                    font_style: 'H3'
                MDLabel:
                    pos_hint: {'center_y':0.2}
                    halign: 'center'
                    text: ''
                    id: output_text
                    theme_text_color: "Custom"
                    text_color: 0, 1, 0, 1

'''
from kivymd.uix.button import MDIconButton
from kivymd.uix.tooltip import MDTooltip
class TooltipMDIconButton(MDIconButton, MDTooltip):
    pass


class ProfilePicture(FitImage):
    newpic = StringProperty()

import os
from kivy.clock import Clock


class Example(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,

        )

    def nn(self):
        self.file_manager = MDFileManager()
        self.file_manager.exit_manager = self.exit_manager
        self.file_manager.select_path = self.select_path
        self.root.ids.edit_profile_pic.disabled = False

    def build(self):
        Clock.schedule_once(lambda x: self.nn(), 3)


        self.help_string = Builder.load_string(KV)
        return self.help_string
    def cover(self):
        self.im = builder.load_string(KV)
        return (self.im)

    def chpic(self, new):
        if os.path.isfile(new) == True:
            self.root.ids.profile_pic.source = new
            print("The picture on 'id: profile_pic' was changed to:", self.root.ids.profile_pic.source)

    def file_manager_open_for_profile(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):

        self.exit_manager()
        print(path)
        if os.path.isfile(path) == True:
            Clock.schedule_once(lambda x: self.chpic(path), 1)
        # toast(path) #here the location for the image file will be returned
        return path

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def predict(self):
        picture = self.im.get_screen('Studio').profile_pic
        url = f'https://localhost:21264/'
        self.request = UrlRequest(url=url, on_success=self.res, ca_file=cfi.where(), verify=True)

    def res(self, *args):
        self.data = self.request.result
        ans = self.data
        self.help_string.get_screen('Studio').ids.output_text.text = ans['predict']


Example().run()
