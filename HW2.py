from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

url = 'https://perm.hh.ru/search/vacancy'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
searching_vacancy = 'Machine learning engineer'
page = 0
params = {'text': searching_vacancy,
          'items_on_page': 20,
          'page': page}

response = requests.get(url, headers=headers, params=params)
soup = bs(response.text, 'html.parser')

all_vacancies_data = []

try:
    last_page = int(soup.find_all('a',{'data-qa':'pager-page'})[-1].text)
except:
    last_page = 1

for i in range(last_page):

    vacancies = soup.find_all('div', {'class': 'vacancy-serp-item-body'})

    for vacancy in vacancies:

        vacancy_data = {}
        vacancy_title = vacancy.find('a', {'data-qa': "vacancy-serp__vacancy-title"})
        vacancy_data['name'] = vacancy_title.getText()
        vacancy_data['link'] = vacancy_title['href']
        vacancy_data['site'] = 'https://perm.hh.ru/'

        vacancy_salary = vacancy.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"})
        if vacancy_salary is None:
            min_salary = None
            max_salary = None
            currency = None
        else:
            vacancy_salary = vacancy_salary.getText()
            if vacancy_salary.startswith('до'):
                max_salary = int("".join([s for s in vacancy_salary.split() if s.isdigit()]))
                min_salary = None
                currency = vacancy_salary.split()[-1]

            elif vacancy_salary.startswith('от'):
                max_salary = None
                min_salary = int("".join([s for s in vacancy_salary.split() if s.isdigit()]))
                currency = vacancy_salary.split()[-1]

            else:
                max_salary = int("".join([s for s in vacancy_salary.split('–')[1] if s.isdigit()]))
                min_salary = int("".join([s for s in vacancy_salary.split('–')[0] if s.isdigit()]))
                currency = vacancy_salary.split()[-1]
        vacancy_data['max_salary'] = max_salary
        vacancy_data['min_salary'] = min_salary
        vacancy_data['currency'] = currency
# Пыталась собрать ЗП другими способами, но ничего толкового не вышло, взяла из разбора ДЗ.
# Но не поняла, как обработался вариант здесь (а он, вроде как, обработался корректно): https://perm.hh.ru/vacancy/55529997?from=vacancy_search_list&hhtmFrom=vacancy_search_list&query=Machine%20learning%20engineer%27
        all_vacancies_data.append(vacancy_data)

    params['page'] = params['page'] + 1
    response = requests.get(url, headers=headers, params=params)
    soup = bs(response.text, 'html.parser')

pprint(all_vacancies_data)