from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

class TitleBox(BoxLayout):
    lbl = StringProperty('')

class PopupBox(Widget):
    def __init__(self, **kwargs):
        self.title = kwargs['title']
        self.on_done = kwargs['on_done']
        if 'ctx' in kwargs:
            self.ctx = kwargs['ctx']
        else:
            self.ctx = []
        super(PopupBox, self).__init__(**kwargs)

    def btn_done(self):
        self.on_done(*self.ctx)
        self.popup.dismiss()

    def open(self):
        self.popup.open()

    def close(self):
        self.popup.dismiss()

class InputBox(PopupBox):
    def btn_done(self):
        self.ctx.insert(0,  self.value.text)
        super(InputBox, self).btn_done()

class ConfirmBox(PopupBox):
    pass

class SelectBox(PopupBox):
    def __init__(self, **kwargs):
        super(SelectBox, self).__init__(**kwargs)
        values = kwargs['values']
        default = kwargs['default']
        for val in values:
            self.combo.values.append(val)
        self.combo.text = default

    def btn_done(self):
        self.ctx.insert(0,  self.combo.text)
        super(SelectBox, self).btn_done()

