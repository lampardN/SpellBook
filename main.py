from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown

import sqlite3

from kivy.core.window import Window
Window.size = (1080//3, 2160//3)

Characters = []
WindowWidget = []
Classes = ['Бард', 'Жрец', 'Друид', 'Паладин', 'Следопыт', 'Чародей\nВолшебник']

db = sqlite3.connect('SpellBook.db')
cursor = db.cursor()


class MainWindow(GridLayout):
    label = ObjectProperty()
    gridArea = ObjectProperty()
    scrollView = ObjectProperty()
    addbutton = ObjectProperty()


    def start(self):
        self.label.text = "Персонажи"
        self.gridArea.bind(minimum_height=self.gridArea.setter('height'))

    def addCharacter(self, widget):
        global cursor, db
        Characters[-1].delbutton.bind(on_release=self.delCharacter)
        Characters[-1].create()
        self.gridArea.add_widget(Characters[-1])

        cursor.execute('INSERT INTO Characters VALUES (?, ?, ?)', [(Characters[-1].name),
                                                                    (Characters[-1].Class),
                                                                    ('')])
        db.commit()


    def delCharacter(self, widget):
        global cursor, db
        for Character in Characters:
            if Character.delbutton == widget:
                self.gridArea.remove_widget(Character)
                cursor.execute('DELETE FROM Characters WHERE name=? AND class=?', [(Character.name), (Character.Class)])
                db.commit()
                del Character
                break



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

    def start(self):
        self.buttons = [self.button1, self.button2, self.button3, self.button4, self.button5, self.button6]
        for i in range(6): self.buttons[i].text = Classes[i]

    def setClass(self, button):
        if button.status:
            button.background_color = [255, 0, 0, 255]
        else:
            button.background_color = [0, 255, 0, 255]
        button.status = not(button.status)
        Characters[-1].CharacterClasses[button.text.replace('\n','')] = not(Characters[-1].CharacterClasses[button.text.replace('\n','')])

    def onFocus(self, widget, value):
        if not(value):
            Characters[-1].name = self.nameInput.text

    def switchColor(self, button):
        if button.status:
            button.background_color = [255, 0, 0, 255]
        else:
            button.background_color = [0, 255, 0, 255]
        button.status = not(button.status)


class CharacterFrame(BoxLayout):
    delbutton = ObjectProperty()
    nameLabel = ObjectProperty()
    name = ''
    Class = ''
    CharacterClasses = {}

    def start(self):
        self.CharacterClasses = {
        'Бард': False,
        'Жрец': False,
        'Друид': False,
        'Паладин': False,
        'Следопыт': False,
        'ЧародейВолшебник': False,
        }

    def create(self):
        name = self.name+' '
        keys = list(self.CharacterClasses.keys())
        for key in keys:
            if self.CharacterClasses[key]:
                self.Class += key + ' '
                name += key[0]+', '
        self.nameLabel.text = name[:-2]
        self.Class = self.Class[:-1]


    def touch(self):
        print(1)



class Conteiner(GridLayout):
    def start(self):
        mainwindow = MainWindow()
        mainwindow.start()
        mainwindow.addbutton.bind(on_release=self.switchToCharacteristicWindow)
        WindowWidget.append(mainwindow)

        CharacteristicWindow = CharacterCharacteristic()
        CharacteristicWindow.start()

        CharacteristicWindow.acceptButton.bind(on_release=mainwindow.addCharacter)
        CharacteristicWindow.acceptButton.bind(on_release=self.switchToMainWindow)

        CharacteristicWindow.cancelButton.bind(on_release=self.switchToMainWindow)

        CharacteristicWindow.button1.bind(on_release=CharacteristicWindow.setClass)
        CharacteristicWindow.button2.bind(on_release=CharacteristicWindow.setClass)
        CharacteristicWindow.button3.bind(on_release=CharacteristicWindow.setClass)
        CharacteristicWindow.button4.bind(on_release=CharacteristicWindow.setClass)
        CharacteristicWindow.button5.bind(on_release=CharacteristicWindow.setClass)
        CharacteristicWindow.button6.bind(on_release=CharacteristicWindow.setClass)

        CharacteristicWindow.nameInput.bind(focus=CharacteristicWindow.onFocus)

        WindowWidget.append(CharacteristicWindow)

        self.add_widget(mainwindow)

    def switchToCharacteristicWindow(self, button):
        self.remove_widget(WindowWidget[0])
        self.add_widget(WindowWidget[1])
        Characters.append(CharacterFrame())
        Characters[-1].start()

    def switchToMainWindow(self, button):
        if button == WindowWidget[1].cancelButton: Characters.pop(-1)
        WindowWidget[1].nameInput.text = ''
        for button in WindowWidget[1].buttons:
            if button.status:
                WindowWidget[1].switchColor(button)
        self.remove_widget(WindowWidget[1])
        self.add_widget(WindowWidget[0])

class SpellBookApp(App):
    def build(self):
        conteiner = Conteiner()
        conteiner.start()
        return conteiner


if __name__ == '__main__':
    SpellBookApp().run()
