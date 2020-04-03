import requests
from pprint import pprint
from bs4 import BeautifulSoup
URL = 'https://pathfinder-wiki.ru/spells/page/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.105', 'accept': 'application/json, text/javascript, */*; q=0.01', 'accept-language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'accept-encoding': 'gzip, deflate, br'}
SpellList = []


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_characteristic(html, name):
    soup = BeautifulSoup(html, 'html.parser')
    characteristics = soup.find_all('section', class_='post_content')
    for characteristic in characteristics:
        parameters = characteristic.find_all('p')

        class_ = {'бард': False,
                  'жрец': False,
                  'друид': False,
                  'паладин': False,
                  'следопыт': False,
                  'чародей/волшебник': False}
        x = parameters[1].text.split()[1:]
        for i in range(0, len(x), 3):
            if x[i].lower() in class_.keys():
                class_[x[i]] = True

        level = [1000000000]
        for i in range(2, len(x), 3):
            num = ''
            for j in x[i]:
                if j in '0123456789':
                    num += j
            if num == '': continue
            level.append(int(num))
        level = str(min(level))

        time = ''
        x = parameters[2].text.split()[2:]
        for i in range(len(x)): time += x[i] + ' '

        target = ''
        x = parameters[5].text.split()
        for i in range(1, len(x)):
            target += x[i] + ' '

        distance = ''
        x = parameters[4].text.split()
        for i in range(1, len(x)):
            distance += x[i] + ' '

        duration = ''
        x = parameters[6].text.split()
        for i in range(1, len(x)):
            duration += x[i] + ' '

        test = ''
        x = parameters[7].text.split()
        for i in range(1, len(x)):
            test += x[i] + ' '

        description = ''
        for i in range(8, len(parameters)):
            text = parameters[i].text
            try:
                x = parameters[i].find_all('span', class_='glossary-tooltip-text')
                for y in x:
                    text = text.replace(y.text, '')
                description += text
            except: description += text

        SpellList.append(
            {'Spell': name,
             'Class': class_,
             'Level': level,
             'School': parameters[0].text.split()[1],
             'Components': parameters[3].text[parameters[3].text.find(':')+2:],
             'Target': target,
             'Distance': distance,
             'Duration': duration,
             'Test': test,
             'Resistance': 0,
             'Time': time,
             'Description': description
             }
        )


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    spells = soup.find_all('td', class_='cat-hadding')
    for spell in spells:
        r = requests.get(spell.find('a').get('href'), headers=HEADERS)
        get_characteristic(r.text, spell.text.strip())


def parse():
    for i in range(2, 22): #max=22
        html = get_html(URL+f'{i}/')
        if html.status_code == 200:
            get_content(html.text)
        else:
            print('Error')


parse()

import sqlite3
db = sqlite3.connect('SpellBook.db')
cursor = db.cursor()
for spell in SpellList:
    cursor.execute('INSERT INTO Spells VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', [spell['Spell'],
                                                                                     spell['Level'],
                                                                                     spell['School'],
                                                                                     spell['Components'],
                                                                                     spell['Target'],
                                                                                     spell['Distance'],
                                                                                     spell['Duration'],
                                                                                     spell['Test'],
                                                                                     spell['Resistance'],
                                                                                     spell['Time'],
                                                                                     spell['Description'],
                                                                                     spell['Class']['бард'],
                                                                                     spell['Class']['жрец'],
                                                                                     spell['Class']['друид'],
                                                                                     spell['Class']['паладин'],
                                                                                     spell['Class']['следопыт'],
                                                                                     spell['Class']['чародей/волшебник']])
    db.commit()
