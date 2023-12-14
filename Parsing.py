import requests
from bs4 import BeautifulSoup
import sqlite3

# Парсинг rabota19.ru
url = 'https://rabota19.ru/vacancy/search/?&page=1'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

data = soup.find_all('tr')

for i in data:
    try:
        name = i.find('div', class_='title14 strong').text.strip()
    except AttributeError:
        continue
    salary = i.find('td', class_='title14').text.replace("от", "").replace('до', ' -').strip()
    description = i.find_all('div', class_='small')[-1].text
    url = 'https://rabota19.ru' + i.find("a").get("href")
#    print(name + '\n' + salary + '\n' + description + '\n' + url + '\n\n')

page = soup.find_all('a', class_='page')
all_page = page[-2].text
print(all_page)

# Создание базы данных SQLite
connection = sqlite3.connect('my_base.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Vacancies (
id INTEGER PRIMARY KEY,
vac TEXT NOT NULL,
text TEXT,
salary INTEGER,
url TEXT NOT NULL
)
''')
connection.commit()
connection.close()


# Добавление информации в БД
def add_bd():
    connect = sqlite3.connect('my_base.db')
    cur = connect.cursor()
    cur.execute('INSERT INTO Vacancies (vac, text, salary, url) VALUES (?, ?, ?, ?)', (name, description, salary, url))
    connect.commit()
    connect.close()


# add_bd()


# Удаление информации из БД
def del_bd(vac_id):
    connect = sqlite3.connect('my_base.db')
    cur = connect.cursor()
    cur.execute("DELETE FROM Vacancies WHERE id = ?", (vac_id,))
    connect.commit()
    connect.close()

# del_bd(4)
