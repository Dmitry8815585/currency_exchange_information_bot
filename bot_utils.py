import os
import sqlite3

from aiogram import Bot
from aiogram.types import ParseMode
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)

LIMIT = 10  # limit of result list


def add_city_id_for_user(value, chat_id):
    try:
        with sqlite3.connect('currency_database.db') as conn:
            c = conn.cursor()
            c.execute(
                "SELECT id FROM cities WHERE city_name = ?",
                (value.capitalize(),)
            )
            city_id = c.fetchone()
            if city_id:
                c.execute(
                   "UPDATE users SET city_id = ? WHERE chat_id = ?",
                   (city_id[0], chat_id)
                )
                conn.commit()
                print("[INFO] City ID added for user.")
            else:
                print("[INFO] City not found.")
    except Exception as e:
        print(f'[INFO] Error: {e}')


def get_city_for_user(chat_id):
    try:
        with sqlite3.connect('currency_database.db') as conn:
            c = conn.cursor()
            c.execute(
                """SELECT cities.city_name
                   FROM users
                   JOIN cities ON users.city_id = cities.id
                   WHERE users.chat_id = ?""",
                (chat_id,)
            )
            city_name = c.fetchone()[0]
            return city_name
    except Exception as e:
        print(f'[INFO] Error: {e}')


def get_cities_from_db() -> list:
    try:
        with sqlite3.connect('currency_database.db') as conn:
            c = conn.cursor()
            c.execute(
                """SELECT city_name FROM cities
                """
            )
            return [city_tuple[0].lower() for city_tuple in c.fetchall()]
    except Exception as e:
        print(f'[INFO] Error: {e}')


def isert_user_into_db(chat_id, first_name, username):
    try:
        with sqlite3.connect('currency_database.db') as conn:
            c = conn.cursor()

            c.execute(
                """INSERT INTO users (chat_id, username, first_name)
                VALUES (?, ?, ?)""",
                (chat_id, username, first_name)
            )
            conn.commit()
            print('[INFO] User added to database.')
    except Exception as e:
        print(f'[INFO] User already in db. error: {e}')


def add_currency_to_user(chat_id, currency):
    try:
        with sqlite3.connect('currency_database.db') as conn:
            c = conn.cursor()

            c.execute(
                """UPDATE users
                   SET currency = ?
                   WHERE chat_id = ?""",
                (currency, chat_id)
            )
            conn.commit()
            print('[INFO] Currency added to user.')
    except Exception as e:
        print(f'[INFO] Error occurred: {e}')


async def get_currency_and_send_message(
        chat_id, buy_or_sell, select_new_search
):
    try:
        with sqlite3.connect('currency_database.db') as conn:
            c = conn.cursor()
            c.execute(
                "SELECT currency FROM users WHERE chat_id = ?",
                (chat_id,)
            )
            user_currency = c.fetchone()[0]

            c.execute(
                "SELECT city_id FROM users WHERE chat_id = ?",
                (chat_id,)
            )
            city_id = c.fetchone()[0]

            sort_direction = "DESC" if buy_or_sell == "buy" else "ASC"

            c.execute(
                '''SELECT banks.bank_name, branches.address, branches.{}_{}
                   FROM branches
                   JOIN banks ON branches.bank_id = banks.id
                   WHERE city_id = ?
                   ORDER BY branches.{}_{} {}
                   LIMIT ? '''.format(
                       user_currency, buy_or_sell, user_currency,
                       buy_or_sell, sort_direction
                    ),
                (city_id, LIMIT)
            )
            rows = c.fetchall()
            if rows:
                buy_sell_dict = {'buy': 'покупают', 'sell': 'продают'}

                message = f"<b>Банки {buy_sell_dict[buy_or_sell]}:</b>\n\n"
                for row in rows:
                    message += f"<i>{row[0]}</i> - {row[1]} - {row[2]}\n\n"
            else:
                message = "По вашему запросу ничего не найдено."

            await bot.send_message(
                chat_id, message,
                reply_markup=select_new_search,
                parse_mode=ParseMode.HTML
            )
    except Exception as e:
        print(f'[INFO] Error occurred: {e}')


def main():
    pass


if __name__ == '__main__':
    main()