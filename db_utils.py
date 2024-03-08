import sqlite3


def create_tables():
    with sqlite3.connect('currency_database.db') as conn:
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS cities
                    (id INTEGER PRIMARY KEY,
                    city_name TEXT,
                    slag TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS banks
                    (id INTEGER PRIMARY KEY,
                    bank_name TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS branches
                    (id INTEGER PRIMARY KEY,
                    city_id INT,
                    bank_id INT,
                    address TEXT,
                    usd_buy REAL,
                    usd_sell REAL,
                    eur_buy REAL,
                    eur_sell REAL,
                    rub_buy REAL,
                    rub_sell REAL,
                    FOREIGN KEY (city_id) REFERENCES cities(id),
                    FOREIGN KEY (bank_id) REFERENCES banks(id))''')

        c.execute('''CREATE TABLE IF NOT EXISTS users
            (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            city_id INT NUL,
            username TEXT,
            first_name TEXT,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            currency TEXT,
            FOREIGN KEY (city_id) REFERENCES cities(id)
            )''')

        conn.commit()
        print('[INFO] All tables are created.')


def clear_database():
    """Delete all data from database."""
    with sqlite3.connect('currency_database.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM branches")
        c.execute("DELETE FROM banks")
        c.execute("DELETE FROM cities")
        conn.commit()
        print('[INFO] All data is deleted.')


def clear_users():
    """Delete all users from database."""
    with sqlite3.connect('currency_database.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM users")
        conn.commit()
        print('[INFO] All users are deleted.')


def insert_data_into_db(data):
    with sqlite3.connect('currency_database.db') as conn:
        c = conn.cursor()

        for entry in data:
            city_name = entry["City_name"]
            bank_name = entry["Bank_name"]
            city_slag = entry["City_slag"]

            c.execute(
                "SELECT id FROM cities WHERE city_name = ?", (city_name,)
            )
            city_row = c.fetchone()
            if not city_row:
                c.execute(
                    "INSERT INTO cities (city_name, slag) VALUES (?, ?)",
                    (city_name, city_slag)
                )
                city_id = c.lastrowid
            else:
                city_id = city_row[0]

            c.execute("SELECT id FROM banks WHERE bank_name = ?", (bank_name,))
            bank_row = c.fetchone()
            if not bank_row:
                c.execute(
                    "INSERT INTO banks (bank_name) VALUES (?)", (bank_name,)
                )
                bank_id = c.lastrowid
            else:
                bank_id = bank_row[0]

            for currency in entry["currencies"]:
                address = currency["address"]
                usd_buy = currency["usd"]["buy"]
                usd_sell = currency["usd"]["sell"]
                eur_buy = currency["eur"]["buy"]
                eur_sell = currency["eur"]["sell"]
                rub_buy = currency["rub"]["buy"]
                rub_sell = currency["rub"]["sell"]

                c.execute(
                    '''INSERT INTO branches
                    (city_id, bank_id, address, usd_buy, usd_sell,
                    eur_buy, eur_sell, rub_buy, rub_sell)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (city_id, bank_id, address, usd_buy, usd_sell,
                        eur_buy, eur_sell, rub_buy, rub_sell)
                )

        conn.commit()
        print('[INFO] Data added to database.')


def main():
    create_tables()
    # clear_users()


if __name__ == '__main__':
    main()
