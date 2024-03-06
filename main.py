import datetime
import json
import re
from time import sleep
from bs4 import BeautifulSoup
import requests
from db import clear_database, insert_data_into_db

import os
from dotenv import load_dotenv

from get_cites import parse_cities

load_dotenv()


URL = os.getenv("URL")
USER_AGENT = os.getenv("USER_AGENT")
ACCEPT = os.getenv("ACCEPT")

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": ACCEPT
}


def time_decorator(func):
    def wrapper(*args):
        start_time = datetime.datetime.now()
        func(*args)
        duration = datetime.datetime.now() - start_time
        print(f'[INFO] Execution time is: {duration}')
    return wrapper


def parse_currency(response, id: str) -> list:
    """"Return data of bank wiht bank_id=id."""
    banks_data = []

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
        usd_buy, usd_sell, eur_buy, eur_sell, rub_buy, rub_sell = [
            span.text for span in spans[:6]
        ]

        bank_data["address"] = address.text.strip()
        bank_data["usd"] = {"buy": usd_buy, "sell": usd_sell}
        bank_data["eur"] = {"buy": eur_buy, "sell": eur_sell}
        bank_data["rub"] = {"buy": rub_buy, "sell": rub_sell}

        banks_data.append(bank_data)

    return banks_data


def parsing_data(city_name, city_slag) -> list:
    """Return list with data of currancy."""
    response = requests.get(url=URL+city_slag, headers=HEADERS)
    soup = BeautifulSoup(response.text, "lxml")

    matches = re.findall(r'id="filial-row-(\d+)"', str(soup))

    banks_info = []

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
    return banks_info


@time_decorator
def main():
    parse_cities()
    try:
        with open('cites.json', 'r') as file:
            data = json.load(file)
            clear_database()
            count = 0
            for city_name, city_slag in data.items():
                insert_data_into_db(
                    parsing_data(city_name, city_slag)
                )
                sleep(2)
                count += 1
        print(f'Iteration amount is: {count}')
    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    main()
