# Prrogrammer salary

Script calculate average salary for top-10 programmer languages from [HeadHanter](https://ekaterinburg.hh.ru/) and [SuperJob](https://www.superjob.ru/) vacansies.

## Installing

- Python3 must be installed.
- Clone repository:
```Bash
git clone https://github.com/CloudCirus/programmer_salary.git
```
- Create enviroment with venv or other source:
```Bash
Python3 -m venv your_enviroment_name
```
- install requirements:
```Bash
pip install -r requirements.txt
```
- Create `.env` file with var for [superjob](https://api.superjob.ru/register) api key:
```
SJ_SECRET_KEY=your_superjob_api_key
```

## Get started

- Run from terminal:
```Bash
python3 main.py
```

## Project goals 

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/)