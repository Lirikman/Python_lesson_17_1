from flask import Flask, render_template, request, redirect
import sqlite3
import requests
from bs4 import BeautifulSoup
from time import sleep

app = Flask(__name__)

# Создание базы данных SQLite
connection = sqlite3.connect('my_base.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Vacancies (
id INTEGER PRIMARY KEY,
vac TEXT NOT NULL,
text TEXT,
salary INTEGER,
contacts INTEGER,
url TEXT NOT NULL
)
''')
connection.commit()
connection.close()


# Удаление информации из БД
def del_bd(vac_id):
    connect = sqlite3.connect('my_base.db')
    cur = connect.cursor()
    cur.execute("DELETE FROM Vacancies WHERE id = ?", (vac_id,))
    connect.commit()
    connect.close()


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/parsing.html', methods=['POST', 'GET'])
def parsing():
    if request.method == 'POST':
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
        # Всего страниц
        url = 'https://rabota19.ru/vacancy/search/?&page=1'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        page = soup.find_all('a', class_='page')
        all_page = page[-2].text
    else:
        return render_template('parsing.html')


@app.route('/base.html', methods=['POST', 'GET'])
def resume():
    return render_template('base.html')


@app.route('/vacancies.html', methods=['POST', 'GET'])
def vac():
    if request.method == 'POST':
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}

        # Список всех ссылок на вакансии
        list_url = []
        count = request.form['number']
        url = f'https://rabota19.ru/vacancy/search/?&page={count}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find_all('div', class_='title14 strong')
        for i in data:
            list_url.append('https://rabota19.ru' + i.find("a").get('href'))

            # Информация о вакансии
        for card_url in list_url:
            response = requests.get(card_url, headers=headers)
            sleep(1)
            soup = BeautifulSoup(response.text, 'lxml')
            data = soup.find('div', class_='main-content')
            try:
                name = data.find("h1", class_='red').text.strip()
                salary = data.find('div', class_='title14').text.replace("от", "").replace('до', ' -').strip()
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
                tmp_1 = data.find_all('div', class_='margin3')[1].text.strip()
                phone = ''
                if tmp_1.startswith('Телефон: '):
                    phone = tmp_1
                else:
                    phone = data.find_all('div', class_='margin3')[2].text.strip()
                    #               print(name + '\n' + salary + '\n' + description + phone + '\n' + card_url + '\n\n'

                    # Добавление информации в БД
                connect = sqlite3.connect('my_base.db')
                cur = connect.cursor()
                cur.execute('INSERT INTO Vacancies (vac, text, salary, contacts, url) VALUES (?, ?, ?, ?)',
                            (name, description, salary, phone, url))
                try:
                    connect.commit()
                    connect.close()
                except:
                    connect.rollback()
                    return 'Ошибка добавления в БД. Попробуйте снова'
            except:
                continue
    else:
        connect = sqlite3.connect('my_base.db')
        cur = connect.cursor()
        all_vac = cur.fetchall()
        return render_template('/vacancies.html')


if __name__ == '__main__':
    app.run(debug=True)
