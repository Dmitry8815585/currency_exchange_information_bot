# Проект: Телеграм-бот лучших курсов валют

## Telegram: [@belpost_tracker_status_bot](https://t.me/exchange_rates_byn_usd_eur_bot)

## Стек навыков проекта:

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Telegram API](https://img.shields.io/badge/Telegram_API-26A5E4?style=for-the-badge&logo=telegram&logoColor=white) ![Logging](https://img.shields.io/badge/Logging-292929?style=for-the-badge&logo=logging&logoColor=white) ![API Requests](https://img.shields.io/badge/API_Requests-009688?style=for-the-badge&logo=requests&logoColor=white)![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)![aiogram](https://img.shields.io/badge/aiogram-009688?style=for-the-badge&logo=requests&logoColor=white)![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-009688?style=for-the-badge&logo=requests&logoColor=white)


## Описание проекта

Этот бот покажет для Вас места с лучшим курсом в выбранном Вами городе. Курсы обновляются один раз в час. Результат сортируется от самого выгодного курса для Вас. Бот работает с банками Республики Беларусь.

## Как использовать

1. Подключитесь к боту, отправив команду /start.
2. Бот запросит у вас название города для поиска.
3. Бот запросит у вас название валюты.
4. Бот запросит вид сделки (купить продать).
5. Бот пришлет отсортированный результат с названием банков, адресами и курсом валюты.

## Важно

1. Бот использует базу данных SQLite для хранения данных.
2. Для периодического парсинга курсов используется модуль threading, для многопоточности, в частности, threading.
3. Бот реализован через Aiogram.
3. Все настройки проекта в файле config.py.
3. События логируются в файл app.log
