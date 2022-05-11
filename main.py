# Библиотеки для работы бота
import json

import aiogram.types
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State

# Библиотеки для работы с БД
import os
import psycopg2
from psycopg2.extras import Json

# Прочее
from configuration import *
from users_states import *
from new_visit import *
from med_card_info_pat import *
from info_about_doc_list import *

# Команды для бота
async def set_commands(bot: bot):
    commands = [
        aiogram.types.BotCommand(command="/doctors_list", description='список всех врачей в нашей клинике')
    ]
    bot.set_my_commands(commands)

@dp.message_handler(commands=['start'], state= '*')
async def send_welcome(msg: types.Message):
    await bot.send_message(msg.from_user.id, f'Здравствуйте, {msg.from_user.first_name}! Чтобы узнать всё, что я умею, отправьте команду /help !')

@dp.message_handler(commands=['help'], state= '*')
async def send_help(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Список того, что я умею: \n'
                           '/doctors_list - список всех врачей в нашей клинике \n'
                            '/med_card_info Информация о вашей медицинской карте \n'
                            '/info_doctors_spec Найти докторов интересующей вас специализации \n'
                            '/new_visit_doc Записаться к доктору \n'
                            '/get_info_M10 Получить расшифровку болезни')

@dp.message_handler(commands=['close_chat'], state= '*')
async def close_chatbot(msg: types.Message):
    await bot.send_message(msg.from_user.id,
                           f'До свидания, {msg.from_user.first_name}! Не болейте'
                           f'\n А если заболели, отправьте команду /start и записывайтесь к нашим врачам'
                           f'\n Вылечим всех! :)')
    await dp.storage.close()
    await dp.storage.wait_closed()

@dp.message_handler(commands=['get_info_M10'], state= '*')
async def get_info_M10(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Введите шифр болезни, которая вас интересует')
    await users_states.get_info_M10.set()

@dp.message_handler(content_types=['text'], state = users_states.get_info_M10)
async def get_info_M10_next_step(msg: types.Message):
    answer = r.get(str(msg.text))
    await bot.send_message(msg.from_user.id,
                           f'Ваш диагноз: {answer.lower()}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
