from kivy.factory import Factory
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

class TitleBox(BoxLayout):
    lbl = StringProperty('')

class PopupBox(Widget):
    def __init__(self, **kwargs):
        self.title = kwargs['title']
        super(PopupBox, self).__init__(**kwargs)

    def open(self):
        self.popup.open()

    def close(self):
        self.popup.dismiss()

class InputBox(PopupBox):
    pass

class ConfirmBox(PopupBox):
    pass

class SelectBox(PopupBox):
    pass

Factory.register('TitleBox', cls=TitleBox)
Factory.register('InputBox', cls=InputBox)
Factory.register('ConfirmBox', cls=ConfirmBox)
Factory.register('SelectBox', cls=SelectBox)

