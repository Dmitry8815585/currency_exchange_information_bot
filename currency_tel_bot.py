from dotenv import load_dotenv
import os

from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import CallbackQuery

from bot_utils import (
    add_city_id_for_user,
    add_currency_to_user,
    get_cities_from_db,
    get_city_for_user,
    get_currency_and_send_message,
    isert_user_into_db
)

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
disp = Dispatcher(bot)

select_currency = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='usd', callback_data='usd'),
            InlineKeyboardButton(text='eur', callback_data='eur'),
            InlineKeyboardButton(text='rub', callback_data='rub'),
        ],
        [
            InlineKeyboardButton(text='Сменить город.', callback_data='start')
        ]
    ]
)

select_action = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Банки продают', callback_data='sell'),
            InlineKeyboardButton(text='Банки покупают', callback_data='buy'),
        ],
        [
            InlineKeyboardButton(text='Сменить город.', callback_data='start')
        ]
    ]
)

select_new_search = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Обновить результат.', callback_data='new_search'
            )
        ]
    ]
)


@disp.message_handler(commands=['start'])
async def start(message: types.Message):
    chat_id = message.chat.id
    first_name = message.chat.first_name if message.chat.first_name else None
    username = message.chat.username if message.chat.username else None
    isert_user_into_db(chat_id, first_name, username)
    await message.answer('Укажите Ваш город.')


@disp.callback_query_handler(lambda query: query.data == 'start')
async def handle_start_callback(callback_query: types.CallbackQuery):
    await bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )
    await start(callback_query.message)


@disp.callback_query_handler(lambda query: query.data in ['sell', 'buy'])
async def handle_buy_sell(callback_query: CallbackQuery):
    chat_id = callback_query.from_user.id
    action = callback_query.data
    await bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )
    await get_currency_and_send_message(
        chat_id, action, select_new_search
    )


@disp.callback_query_handler(lambda query: query.data in ['usd', 'eur', 'rub'])
async def handle_currency_callback(callback_query: types.CallbackQuery):
    currency = callback_query.data
    chat_id = callback_query.from_user.id
    add_currency_to_user(chat_id, currency)
    await bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )
    await bot.send_message(
        callback_query.from_user.id, f'Вы выбрали валюту {currency.upper()}',
        reply_markup=select_action
    )


@disp.callback_query_handler(lambda query: query.data == 'new_search')
async def handle_new_search(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    city = get_city_for_user(chat_id)
    await bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )
    await bot.send_message(
        callback_query.from_user.id,
        f'Ваш город {city} \nвыберете валюту',
        reply_markup=select_currency
    )


@disp.message_handler()
async def handle_text(message: types.Message):
    text = message.text
    print(text)
    if text.lower() in get_cities_from_db():
        add_city_id_for_user(text, message.chat.id)

        prev_message_id = message.message_id - 1

        await bot.delete_message(message.chat.id, prev_message_id)

        await message.answer(
            f'Ваш город {text.capitalize()}\nвыберете валюту',
            reply_markup=select_currency
        )
    else:
        await message.answer(
            'Такого города нет в базе данных.\n'
            'Проверьте название города, возможно вы написали с ошибкой.'
        )


if __name__ == '__main__':
    executor.start_polling(disp)
