from terminaltables import SingleTable

from headhunter import predict_rub_salary_hh
from superjob import predict_rub_salary_sj


def show_table(predicted_salaries: dict, title: str) -> SingleTable:
    rows = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата',
        ]
    ]
    for lang, salaries in predicted_salaries.items():
        rows.append(
            [
                lang,
                salaries.get('vacancies_found'),
                salaries.get('vacancies_processed'),
                salaries.get('average_salary'),
            ]
        )
    print(SingleTable(rows, title).table)


def main() -> None:
    langs = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C++',
        'C',
        'C#',
    ]
    hh_salaries = predict_rub_salary_hh(langs)
    sj_salaries = predict_rub_salary_sj(langs)

    show_table(hh_salaries, 'HeadHunter Moscow')
    show_table(sj_salaries, 'SuperJob Moscow')


if __name__ == '__main__':
    main()
