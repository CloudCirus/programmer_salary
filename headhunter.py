import json
from typing import Union

import requests
from requests.exceptions import HTTPError


def get_vacancies(language: str, page: int = 0, per_page: int = 1) -> json:
    url = 'https://api.hh.ru/vacancies/'
    payload = {
        'text': f'программист {language}',
        'area': 1,
        'page': page,
        'per_page': per_page,
    }
    resp = requests.get(url, params=payload)
    resp.raise_for_status()
    return resp.json()


def collect_vacancies(language: str, per_page: int = 100) -> dict:
    vacancies_info = get_vacancies(language)
    vacansies_found = vacancies_info.get('found')
    page_nums = vacansies_found // per_page + 1

    all_vacancies = []
    try:
        for page in range(page_nums):
            vacancies_per_page = get_vacancies(
                language, page, per_page).get('items')
            for vacancy in vacancies_per_page:
                all_vacancies.append(vacancy)
    except HTTPError:
        print(f'Maximum vacancies for {language} collected...')

    return {'found': vacansies_found, 'vacancies': all_vacancies}


def calculate_salary(vacancy: dict) -> Union[float, None]:
    salary_info = vacancy.get('salary')
    if not salary_info:
        return None

    currency = salary_info.get('currency')
    if not currency:
        return None

    start = salary_info.get('from')
    end = salary_info.get('to')
    if start and end:
        salary = (start + end) / 2
    if start and not end:
        salary = start * 1.2
    else:
        salary = end * 0.8
    return salary


def collect_salary(language: str) -> dict:
    collected_vacancies = collect_vacancies(language)

    vacancies_found = collected_vacancies.get('found')
    vacancies = collected_vacancies.get('vacancies')
    vacancies_processed = []

    for vacancy in vacancies:
        salary = calculate_salary(vacancy)
        if salary:
            vacancies_processed.append(salary)
    processed = len(vacancies_processed)
    avg_salary = sum(vacancies_processed)/processed

    return {
        language: {
            'vacancies_found': vacancies_found,
            'vacancies_processed': processed,
            'average_salary': int(avg_salary)
        }
    }


def predict_rub_salary_hh(langs: list) -> dict:
    collected_salaries = {}
    for lang in langs:
        collected_salaries.update(collect_salary(lang))
    return collected_salaries
