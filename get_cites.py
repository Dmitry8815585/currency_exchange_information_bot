import json
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests

load_dotenv()


URL = os.getenv("URL")
USER_AGENT = os.getenv("USER_AGENT")
ACCEPT = os.getenv("ACCEPT")

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": ACCEPT
}


def parse_cities() -> dict:
    """Return dict and create json with all cities and slags. """
    cities = {}
    try:
        response = requests.get(url=URL, headers=HEADERS)
        soup = BeautifulSoup(response.text, "lxml")
        city_elements = soup.find_all(
            'a', class_="set_city"
        )
        for city in city_elements:
            city_name = city.text.strip()
            city_slug = city['data-slug']
            cities[city_name] = city_slug

        with open('cites.json', 'w') as file:
            json.dump(cities, file, indent=4, ensure_ascii=False)
        print('[INFO] Data recуived.')
    except requests.HTTPError as e:
        print(f"[ERROR] HTTP error occurred: {e}")
        return {}
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
        return {}


def main():
    parse_cities()


if __name__ == '__main__':
    main()
