from bs4 import BeautifulSoup
from requests import get


def get_countries():
    url = 'https://www.focus-economics.com/countries'

    raw = get(url).text
    soup = BeautifulSoup(raw, features='html.parser')
    countries_table = soup.find_all('div', class_='row coutries-list')
    countries = countries_table[0].find_all('li')

    countries_list = [country.text for country in countries]
    return countries_list

def get_data_for_country(country):
    url = 'https://www.focus-economics.com/countries/' + country

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
    return country_data


countries_list = get_countries()
countries_dict = {}
for country in countries_list:
    print(country)
    data = get_data_for_country(country)
    countries_dict[country] = data

print(countries_dict)