import requests
from bs4 import BeautifulSoup

url = 'https://rabota19.ru/vacancy/search/?&page=1'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

data = soup.find('tr')
name = data.find('div', class_='title14 strong').text.strip()
salary = data.find('td', class_='title14').text.replace("от", "").replace('до', ' -')
description = data.find_all('div', class_='small')[-1].text

#url = soup.find("div", class_="title14 strong")

print(description)
#print(data)