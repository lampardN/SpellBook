from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from CharacterFrame import CharacterFrame
from CharacterCharacteristic import CharacterCharacteristic
from MainWindow import MainWindow
from CharacterBook import CharacterBook
from dbController import dbController

from kivy.core.window import Window
Window.size = (1080//3, 2160//3)

Characters = []
WindowWidget = []


class Container(GridLayout):
    def __init__(self):
        super().__init__()
        self.mainWindow = MainWindow()
        self.mainWindow.addbutton.bind(on_release=self.switchToCharacteristicWindow)

        self.CharacteristicWindow = CharacterCharacteristic()
        self.CharacteristicWindow.acceptButton.bind(on_release=self.addCharacter)
        self.CharacteristicWindow.cancelButton.bind(on_release=self.switchToMainWindow)

        self.CharacterBook = CharacterBook()

        WindowWidget.append(self.mainWindow)
        WindowWidget.append(self.CharacteristicWindow)
        WindowWidget.append(self.CharacterBook)

        self.loadCharacters()
        self.add_widget(self.mainWindow)

    def addCharacter(self, button):
        Characters[-1].name = self.CharacteristicWindow.nameInput.text
        for button in self.CharacteristicWindow.buttons:
            Characters[-1].CharacterClasses[button.text] = button.status
        Characters[-1].delbutton.bind(on_release=self.deleteCharacter)
        dbController().addCharacter(Characters[-1])
        Characters[-1].id = dbController().loadCharacters()[-1][0]
        Characters[-1].create()
        self.switchToMainWindow(None)

    def switchToCharacteristicWindow(self, button):
        self.remove_widget(WindowWidget[0])
        self.add_widget(WindowWidget[1])
        Characters.append(CharacterFrame())
        #  Characters[-1].nameLabel.bind(on_touch_down=self.switchToCharacterBook)

    def switchToMainWindow(self, button):
        self.reloadMainWindow()
        if button == WindowWidget[1].cancelButton: Characters.pop(-1)
        WindowWidget[1].nameInput.text = ''
        for button in WindowWidget[1].buttons:
            if button.status:
                WindowWidget[1].switchColor(button)
        self.remove_widget(WindowWidget[1])
        self.add_widget(WindowWidget[0])

    def switchToCharacterBook(self, label, mouse):
        self.remove_widget(WindowWidget[0])
        self.add_widget(WindowWidget[2])

    def reloadMainWindow(self):
        for character in Characters:
            try:
                self.mainWindow.gridArea.remove_widget(character)
            except:
                pass
        for character in Characters:
            self.mainWindow.gridArea.add_widget(character)
            print(character.name, character.nameLabel.text)

    def deleteCharacter(self, button):
        for Character in Characters:
            if Character.delbutton == button:
                dbController().delCharacter(Character)
                self.mainWindow.gridArea.remove_widget(Character)
                dbController().reloadID()
                del Character
                return

    def loadCharacters(self):
        CharactersFromDB = dbController().loadCharacters()
        for Character in CharactersFromDB:
            CurCharacter = CharacterFrame()
            CurCharacter.id = Character[0]
            CurCharacter.name = Character[1]
            CurCharacter.CharacterClasses['Бард'] = Character[2]
            CurCharacter.CharacterClasses['Жрец'] = Character[3]
            CurCharacter.CharacterClasses['Друид'] = Character[4]
            CurCharacter.CharacterClasses['Паладин'] = Character[5]
            CurCharacter.CharacterClasses['Следопыт'] = Character[6]
            CurCharacter.CharacterClasses['Чародей'] = Character[7]
            CurCharacter.CharacterClasses['Волшебник'] = Character[8]
            CurCharacter.create()
            CurCharacter.delbutton.bind(on_release=self.deleteCharacter)
            #  CurCharacter.nameLabel.bind(on_touch_down=self.switchToCharacterBook)
            Characters.append(CurCharacter)
            self.mainWindow.gridArea.add_widget(CurCharacter)


class SpellBookApp(App):
    def build(self):
        container = Container()
        return container


if __name__ == '__main__':
    SpellBookApp().run()
