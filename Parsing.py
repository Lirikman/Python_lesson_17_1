import requests
from bs4 import BeautifulSoup
from time import sleep
import sqlite3


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
# Парсинг rabota19.ru
url = 'https://rabota19.ru/vacancy/search/?&page=1'
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

# Всего страниц на сайте
page = soup.find_all('a', class_='page')
all_page = page[-2].text
print(all_page)

data = soup.find_all('tr')

for i in data:
    try:
#        sleep(2)
        name = i.find('div', class_='title14 strong').text.strip()
        salary = i.find('td', class_='title14').text.replace("от", "").replace('до', ' -').strip()
        description = i.find_all('div', class_='small')[-1].text
        url = 'https://rabota19.ru' + i.find("a").get("href")
        print(name + '\n' + salary + '\n' + description + '\n' + url + '\n\n')
    except AttributeError:
        continue



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
