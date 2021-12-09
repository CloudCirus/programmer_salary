import json
from typing import Union

import requests
from environs import Env
from requests.exceptions import HTTPError


def get_vacancies(language: str, page: int = 0, count: int = 100) -> json:
    env = Env()
    env.read_env()
    sj_token = env.str('SJ_SECRET_KEY')

    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': sj_token,
    }
    payload = {
        'keyword': f'Программист {language}',
        'town': 'Москва',
        'page': page,
        'count': count,
    }
    resp = requests.get(url, headers=headers, params=payload)
    resp.raise_for_status()
    return resp.json()


def collect_vacancies(language: str, count: int = 100) -> dict:
    vacancies_info = get_vacancies(language)
    vacansies_found = vacancies_info.get('total')
    page_nums = vacansies_found // 100 + 1

    all_vacancies = []
    try:
        for page in range(page_nums):
            vacancies_per_page = get_vacancies(
                language, page, count).get('objects')
            for vacancy in vacancies_per_page:
                all_vacancies.append(vacancy)
    except HTTPError:
        print(f'Maximum vacancies for {language} collected...')

    return {'found': vacansies_found, 'vacancies': all_vacancies}


def calculate_salary(salary_info: dict) -> Union[float, None]:
    currency = salary_info.get('currency')
    if not currency:
        return None

    start = salary_info.get('payment_from')
    end = salary_info.get('payment_to')
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


def predict_rub_salary_sj(langs: list) -> dict:
    collected_salaries = {}
    for lang in langs:
        collected_salaries.update(collect_salary(lang))
    return collected_salaries
