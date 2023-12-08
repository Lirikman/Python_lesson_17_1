import requests
from bs4 import BeautifulSoup

url = 'https://rabota19.ru/vacancy/search/?&page=1'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

data = soup.find('tr')
name = data.find('div', class_='title14 strong').text.strip()
salary = data.find('td', class_='title14').text.replace("от", "").replace('до', ' -').strip()
description = data.find_all('div', class_='small')[-1].text
url = 'https://rabota19.ru' + data.find("a").get("href")

#print(data)
print(name)
print(salary)
print(description)
print(url)