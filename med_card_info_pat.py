from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State

# Библиотеки для работы с БД
import os
import psycopg2
from psycopg2.extras import Json

from configuration import *
from users_states import *

@dp.message_handler(commands=['med_card_info'], state= '*')
async def send_mc_info(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Пожалуйста, напишите ваше ФИО и номер телефона в одном сообщении через пробел'
                                             'Пример: Иванов Иван Иванович 7xxxxxxxxxx')
    await users_states.name.set()

@dp.message_handler(content_types=['text'], state=users_states.name)
async def get_mc_info(msg: types.Message):
    name1, name2, name3, phone = msg.text.split()
    name = name1 + ' ' + name2 + ' ' + name3
    db_pg_doc_obj.execute("select data_pat ->'name', data_pat->'address', data_pat->'years', data_pat -> 'phone_number' from patient_test pt "
                          "where data_pat ->> 'phone_number' = %s and data_pat ->> 'name' = %s ", [phone, name])
    result = db_pg_doc_obj.fetchall()

    if not result:
        await bot.send_message(msg.from_user.id, 'Простите, но ваша медицинская карта не найдена \n'
                                                 'Если вы не заводили карту, то вызовите команду /new_med_card \n'
                                                 'Если вы ранее заводили карту, но она не была найдена, обратитесь в службу поддержки')
        await users_states.new_pat.set()
    else:
        reply_message = "Ваши данные из медицинской карты: \n"
        for i, item in enumerate(result):
            reply_message += f' ФИО пациента: {item[0]}; \n Город проживания: {item[1]}; \n Возраст: {item[2]}; \n'
        await bot.send_message(msg.from_user.id, reply_message)


@dp.message_handler(commands=['new_med_card'], state= '*')
async def add_new_pat(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Давайте создадим вашу карту, для этого последовательно ответьте на следующие вопросы: \n'
                                             'Введите ваше ФИО в одной строке в новом сообщении')
    await users_states.new_pat_name.set()

@dp.message_handler(content_types=['text'], state= users_states.new_pat_name)
async def add_new_pat_name(msg: types.Message):
    global name_pat
    name_pat = msg.text
    db_pg_doc_obj.execute("insert into patient_test (data_pat) values ( %s )", [ Json({'name' : name_pat}) ])
    connection_1.commit()
    await bot.send_message(msg.from_user.id, f'Приятно познакомиться,{name_pat}, сколько вам лет?')
    await users_states.new_pat_years.set()

@dp.message_handler(content_types=['text'], state= users_states.new_pat_years)
async def add_new_pat_years(msg: types.Message):
    db_pg_doc_obj.execute("update patient_test "
                          "set data_pat = jsonb_set (data_pat, '{years}', %s)"
                          "where data_pat ->> 'name' = %s",
                          [str(msg.text), name_pat])

    connection_1.commit()
    await bot.send_message(msg.from_user.id, f'Здорово {name_pat}! Напишите адрес, по которому вы проживаете')
    await users_states.new_pat_cities.set()

@dp.message_handler(content_types=['text'], state= users_states.new_pat_cities)
async def add_new_pat_addr(msg: types.Message):
    print(msg.text)
    db_pg_doc_obj.execute('select add_new_patient_info (%s, %s, %s)',
                          [name_pat, '{address}' , Json(msg.text)])
    connection_1.commit()
    await bot.send_message(msg.from_user.id, 'Отлично! И последний вопрос: напишите ваш номер телефона в формате 7xxxxxxxxxx')
    await users_states.new_pat_phone.set()

@dp.message_handler(content_types=['text'], state=users_states.new_pat_phone)
async def add_new_pat_phone(msg: types.Message):
    db_pg_doc_obj.execute('select add_new_patient_info (%s, %s, %s)',
                          [name_pat, '{phone_number}', Json(msg.text)])
    connection_1.commit()
    await bot.send_message(msg.from_user.id,
                           'Отлично! И последний вопрос: напишите ваш номер телефона в формате 7xxxxxxxxxx')
    await users_states.new_pat_phone.set()
    await bot.send_message(msg.from_user.id, "Ваши данные из карты: ")
    db_pg_doc_obj.execute("select data_pat ->'name', data_pat->'address', data_pat->'years', data_pat -> 'phone_number' from patient_test pt "
                          "where data_pat ->> 'phone_number' = %s and data_pat ->> 'name' = %s ", [msg.text, name_pat])
    result = db_pg_doc_obj.fetchall()

    if not result:
        await bot.send_message(msg.from_user.id, 'Простите, но ваша медицинская карта не найдена \n'
                                                 'Если вы не заводили карту, то вызовите команду /new_med_card \n'
                                                 'Если вы ранее заводили карту, но она не была найдена, обратитесь в службу поддержки')
        await users_states.new_pat.set()
    else:
        reply_message = ""
        for i, item in enumerate(result):
            reply_message += f' ФИО пациента: {item[0]}; \n Город проживания: {item[1]}; \n Возраст: {item[2]}; \n Номер: {item[3]}'
        await bot.send_message(msg.from_user.id, reply_message)