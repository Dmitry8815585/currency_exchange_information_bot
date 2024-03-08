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
            InlineKeyboardButton(text='продают', callback_data='sell'),
            InlineKeyboardButton(text='покупают', callback_data='buy'),
        ],
        [
            InlineKeyboardButton(text='Сменить город.', callback_data='start')
        ]
    ]
)


@disp.message_handler(commands=['inline'])
async def get_inline(message: types.Message):
    await message.answer('this is keyboard.', reply_markup=select_currency)


@disp.message_handler(commands=['start'])
async def start(message: types.Message):
    chat_id = message.chat.id
    first_name = message.chat.first_name if message.chat.first_name else None
    username = message.chat.username if message.chat.username else None
    isert_user_into_db(chat_id, first_name, username)
    await message.answer('Укажите Ваш город.')


@disp.callback_query_handler(lambda query: query.data == 'start')
async def handle_start_callback(callback_query: types.CallbackQuery):
    await start(callback_query.message)


@disp.callback_query_handler(lambda query: query.data == 'sell')
async def handle_sell(callback_query: CallbackQuery):
    chat_id = callback_query.from_user.id
    await get_currency_and_send_message(
        chat_id, 'sell', select_currency
    )


@disp.callback_query_handler(lambda query: query.data == 'buy')
async def handle_buy(callback_query: CallbackQuery):
    chat_id = callback_query.from_user.id
    await get_currency_and_send_message(
        chat_id, 'buy', select_currency
    )


@disp.callback_query_handler(lambda query: query.data in ['usd', 'eur', 'rub'])
async def handle_currency_callback(callback_query: types.CallbackQuery):
    currency = callback_query.data
    chat_id = callback_query.from_user.id
    add_currency_to_user(chat_id, currency)
    await bot.send_message(
        callback_query.from_user.id, f'Вы выбрали валюту {currency.upper()}',
        reply_markup=select_action
    )


@disp.message_handler()
async def handle_text(message: types.Message):
    text = message.text
    print(text)
    if text.lower() in get_cities_from_db():
        add_city_id_for_user(text, message.chat.id)

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
