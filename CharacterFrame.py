from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class CharacterFrame(BoxLayout):
    delbutton = ObjectProperty()
    nameLabel = ObjectProperty()
    id = None
    name = ''
    Class = ''
    CharacterClasses = {}

    def __init__(self):
        super().__init__()
        self.CharacterClasses = {
            'Бард': False,
            'Жрец': False,
            'Друид': False,
            'Паладин': False,
            'Следопыт': False,
            'Чародей': False,
            'Волшебник': False
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
