# Библиотеки для работы бота
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Библиотеки для работы с БД
import os
import psycopg2
import redis

TOKENBOT = "---"

# Создание бота

bot = Bot(token= TOKENBOT)
dp = Dispatcher(bot, storage=MemoryStorage())

# Подключение к БД

connection_1 = psycopg2.connect(database= '---', user= '---', host= '---', port= '---', password= '---')
db_pg_doc_obj = connection_1.cursor()
connection_2 = psycopg2.connect(database= '---', user= '---', password= '---', host= '---', port= '---')
db_pg_rb_obj = connection_2.cursor()

# Подключение к Redis

r = redis.StrictRedis(
    host= '---',
    port= ---,
    password='---',
    charset="utf-8",
    decode_responses=True
)
