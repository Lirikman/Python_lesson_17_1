import requests
from bs4 import BeautifulSoup
from time import sleep
import sqlite3

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}


# Парсинг rabota19.ru

# Всего страниц
def get_page():
    url = 'https://rabota19.ru/vacancy/search/?&page=1'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    page = soup.find_all('a', class_='page')
    all_page = page[-2].text
    return all_page


# Список всех ссылок на вакансии
def get_url():
    count = 1
    url = f'https://rabota19.ru/vacancy/search/?&page={count}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find_all('div', class_='title14 strong')
    for i in data:
        card_vac = 'https://rabota19.ru' + i.find("a").get('href')
        yield card_vac


# Информация о вакансии
for card_url in get_url():
    response = requests.get(card_url, headers=headers)
    sleep(1)
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find('div', class_='main-content')
    try:
        name = data.find("h1", class_='red').text.strip()
        salary = data.find('div', class_='title14').text.replace("от", "").replace('до', ' -').strip()
        tmp = data.find_all('div', class_='')
        description = ''
        tmp_des_1 = data.find_all('div')[4].text.strip()
        if tmp_des_1 is not None:
            description += 'График работы: ' + tmp_des_1 + '\n'
        tmp_des_2 = data.find_all('div')[5].text.strip()
        if tmp_des_2 is not None:
            description += tmp_des_2 + '\n'
        else:
            tmp_des_3 = data.find_all('div')[6].text.strip()
            if tmp_des_3 is not None:
                description += tmp_des_3 + '\n'
            else:
                tmp_des_4 = data.find_all('div')[7].text.strip()
                if tmp_des_4 is not None:
                    description += tmp_des_4
        tmp_2 = data.find_all('div', class_='margin3')[1].text.strip()
        phone = ''
        if tmp_2.startswith('Телефон: '):
            phone = tmp_2
        else:
            phone = data.find_all('div', class_='margin3')[2].text.strip()
        print(name + '\n' + salary + '\n' + description + phone + '\n' + card_url + '\n\n')
    except:
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
