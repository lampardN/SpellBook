from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from config import Classes


class CharacterCharacteristic(BoxLayout):
    acceptButton = ObjectProperty()
    cancelButton = ObjectProperty()
    nameInput = ObjectProperty()
    button1 = ObjectProperty()
    button2 = ObjectProperty()
    button3 = ObjectProperty()
    button4 = ObjectProperty()
    button5 = ObjectProperty()
    button6 = ObjectProperty()
    buttons = []

    def __init__(self):
        super().__init__()
        self.buttons = [self.button1, self.button2, self.button3, self.button4, self.button5, self.button6,
                        self.button7]
        for i in range(len(self.buttons)):
            self.buttons[i].text = Classes[i]
            self.buttons[i].bind(on_release=self.setClass)

    def setClass(self, button):
        if button.status:
            button.background_color = [255, 0, 0, 255]
        else:
            button.background_color = [0, 255, 0, 255]
        button.status = not (button.status)

    def switchColor(self, button):
        if button.status:
            button.background_color = [255, 0, 0, 255]
        else:
            button.background_color = [0, 255, 0, 255]
        button.status = not (button.status)
