from bs4 import BeautifulSoup
from requests import get

url = 'https://www.focus-economics.com/countries/albania'

raw = get(url).text

soup = BeautifulSoup(raw, features='html.parser')

rows = soup.find_all('tr')

start = False
country_data = {}
for row in rows:
    if not row.text.find('Population') == -1:
        start = True
    if start:
        columns = row.find_all('td')
        if columns:
            country_data[columns[0].text] = columns[-1].text
        else:
            start = False

print(country_data)