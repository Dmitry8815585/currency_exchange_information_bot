import datetime
import re
import sqlite3
import time

import requests
import schedule
from bs4 import BeautifulSoup

from config import DATABASE_NAME, HEADERS, URL, logger
from currency_tel_bot import start_bot
from db_utils import clear_database, create_tables, insert_data_into_db
from get_cities import parse_cities


def parse_currency(response, id: str) -> list:
    """"Return data of bank wiht bank_id=id."""
    banks_data = []
    try:
        soup = BeautifulSoup(response.text, "lxml")

        rows = soup.find(
            "tr", class_="currencies-courses__row-additional",
            id=f"filial-row-{id}"
        )

        table = rows.find("tbody")
        string = table.find_all("tr")

        for i in string:
            bank_data = {}
            address = i.find_all("a")[0]
            spans = i.find_all("span")

            if len(spans) >= 6:
                usd_buy, usd_sell, eur_buy, eur_sell, rub_buy, rub_sell = [
                    span.text for span in spans[:6]
                ]

                bank_data["address"] = address.text.strip()
                bank_data["usd"] = {"buy": usd_buy, "sell": usd_sell}
                bank_data["eur"] = {"buy": eur_buy, "sell": eur_sell}
                bank_data["rub"] = {"buy": rub_buy, "sell": rub_sell}

                banks_data.append(bank_data)
            else:
                logger.warning(
                    "Not enough currency data available for parsing. id:'{id}'"
                )
    except Exception as e:
        logger.error(
            f"An error occurred while parsing currency: {e}"
        )

    return banks_data


def parsing_data(city_name, city_slag) -> list:
    """Return list with data of currancy."""
    response = requests.get(url=URL+city_slag, headers=HEADERS)
    soup = BeautifulSoup(response.text, "lxml")

    matches = re.findall(r'id="filial-row-(\d+)"', str(soup))

    banks_info = []
    try:
        for match in matches:
            banks_name = soup.find("tr", attrs={"id": f"bank-row-{match}"})
            resul = banks_name.find("span").text.strip()
            branch_amount = banks_name.find(
                "span", class_="currencies-courses__pin"
            ).text.strip()

            banks_info.append(
                {
                    "City_name": city_name,
                    "City_slag": city_slag,
                    "Bank_name": resul,
                    "branch_numbers": branch_amount,
                    "currencies": parse_currency(response, match),
                }
            )
    except Exception as e:
        logger.info(f"An error occurred while parsing data: {e}")

    return banks_info


def main():
    try:
        start_bot()
        create_tables()
        parse_cities()

        def job():
            try:
                now = datetime.datetime.now()
                if now.weekday() < 5:
                    with sqlite3.connect(DATABASE_NAME) as conn:
                        c = conn.cursor()

                        c.execute("SELECT city_name, slag FROM cities")
                        data = c.fetchall()

                    count = 0
                    data_list = []

                    logger.info('Parsing has started.')
                    for city_name, city_slag in data:
                        data_list += parsing_data(city_name, city_slag)
                        count += 1
                        time.sleep(3)  # 3 sec delay
                    clear_database()
                    insert_data_into_db(data_list)

                    logger.info(f'Iteration amount is: {count}')

            except Exception as e:
                logger.error(f'An error occurred: {e}')
                schedule.every(5).minutes.do(job)

        schedule.every().day.at("06:00").do(job)
        schedule.every().day.at("07:00").do(job)
        schedule.every().day.at("08:00").do(job)
        schedule.every().day.at("09:00").do(job)
        schedule.every().day.at("10:00").do(job)
        schedule.every().day.at("11:00").do(job)
        schedule.every().day.at("12:00").do(job)
        schedule.every().day.at("13:00").do(job)
        schedule.every().day.at("14:00").do(job)

        while True:
            schedule.run_pending()
            time.sleep(60)

    except Exception as e:
        logger.error(f'An error occurred: {e}')


if __name__ == '__main__':
    main()
