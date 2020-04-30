import sqlite3


class dbController:

    def __init__(self):
        self.db = sqlite3.connect('SpellBook.db')
        self.cursor = self.db.cursor()

    def loadCharacters(self):
        characters = self.cursor.execute('SELECT * FROM Characters')
        return list(characters)

    def addCharacter(self, character):
        self.cursor.execute('INSERT INTO Characters (Name, Bard, Sacrificer, Druid, Paladin, Ranger, Wizard, Sorcerer, StudiedSpells, PreparedSpells) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',[character.name,
                                                                                character.CharacterClasses['Бард'],
                                                                                character.CharacterClasses['Жрец'],
                                                                                character.CharacterClasses['Друид'],
                                                                                character.CharacterClasses['Паладин'],
                                                                                character.CharacterClasses['Следопыт'],
                                                                                character.CharacterClasses['Чародей'],
                                                                                character.CharacterClasses['Волшебник'],
                                                                                '',
                                                                                ''])
        self.db.commit()

    def delCharacter(self, character):
        self.cursor.execute('DELETE FROM Characters WHERE id=?', [character.id])
        self.db.commit()

    def reloadID(self):
        characters = self.loadCharacters()
        for i in range(1, len(characters)+1):
            self.cursor.execute('UPDATE Characters SET id=? WHERE name=?', [i, characters[i-1][0]])
            self.db.commit()
