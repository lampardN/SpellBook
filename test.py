import sqlite3
db = sqlite3.connect('SpellBook.db')
cursor = db.cursor()
cursor.execute('SELECT * FROM Spells')
SpellList = []
for spell in cursor.fetchall():
    SpellList.append(
    {'Spell': spell[0],
    'Class':list(spell[1].split()),
    'Level': spell[2],
    'School': spell[3],
    'Components': spell[4],
    'Target': spell[5],
    'Distance': spell[6],
    'Duration': spell[7],
    'Test': spell[8],
    'Resistance': spell[9],
    'Description': spell[10]
    }
    )

from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window

class MainApp(App):
    def build(self):
        lbl = Label(text_size=(Window.width, None))
        lbl.text = SpellList[0]['Description']
        return lbl

if __name__ == '__main__':
    MainApp().run()
