import json
from bs4 import BeautifulSoup


def parse_cities() -> dict:
    """Return dict and create json with all cities and slags. """
    cities = {}
    with open("index.html") as file:
        response = file.read()
    soup = BeautifulSoup(response, "lxml")
    city_elements = soup.find_all(
        'a', class_="set_city"
    )
    for city in city_elements:
        city_name = city.text.strip()
        city_slug = city['data-slug']
        cities[city_name] = city_slug

    with open('cites.json', 'w') as file:
        json.dump(cities, file, indent=4, ensure_ascii=False)

    return cities


def main():
    parse_cities()


if __name__ == '__main__':
    main()
