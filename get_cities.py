import sqlite3

import requests
from bs4 import BeautifulSoup

from config import HEADERS, URL, logger


def parse_cities():
    """Get and adding to db all cities and slags."""
    try:
        response = requests.get(url=URL+'minsk', headers=HEADERS)
        soup = BeautifulSoup(response.text, "lxml")
        city_elements = soup.find_all("a", class_="set_city")
        with sqlite3.connect("currency_database.db") as conn:
            c = conn.cursor()
            for city in city_elements:
                city_name = city.text.strip()
                city_slug = city["data-slug"]
                c.execute(
                    "SELECT * FROM cities WHERE city_name = ?", (city_name,)
                )
                existing_city = c.fetchone()
                if existing_city:
                    c.execute(
                        "UPDATE cities SET slag = ? WHERE city_name = ?",
                        (city_slug, city_name)
                    )
                else:
                    c.execute(
                        "INSERT INTO cities (city_name, slag) VALUES (?, ?)",
                        (city_name, city_slug)
                    )
            conn.commit()
        logger.info("Cities data is received.")
    except requests.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


def main():
    pass


if __name__ == "__main__":
    main()
