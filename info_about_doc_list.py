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

@dp.message_handler(commands=['doctors_list'], state= '*')
async def send_shedule(msg: types.Message):
    db_pg_rb_obj.execute(" select sn.iddoc as ID_Доктора, sn.lastname as Фамилия, sn.firstname as Имя, sn.patronymic as Отчество, p.descr as Должность  from stafflist_new sn "
                         "join post p on p.idpost = sn.idpost "
                         "where sn.idpost != 5")
    result = db_pg_rb_obj.fetchall()

    if not result:
        await bot.send_message(msg.from_user.id, "Простите, произошла ошибка, обратитесь в службу поддержки")
    else:
        reply_message = "Список докторов: \n"
        for i, item in enumerate(result):
            reply_message += f'{item[0]} {item[1]} {item[2]} {item[3]} {item[4]} \n'
        await bot.send_message(msg.from_user.id, reply_message)

@dp.message_handler(commands=['info_doctors_spec'], state= '*')
async def get_info_doc_spec(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Введите специализацию врача, к которому вы хотите записаться')
    await users_states.get_doc_spec.set()

@dp.message_handler(content_types=['text'], state= users_states.get_doc_spec)
async def get_info_doc_spec_ans(msg: types.Message):
    db_pg_rb_obj.execute('select * from get_doctrors_spec (%s)', [str(msg.text)])
    result = db_pg_rb_obj.fetchall()

    if not result:
        await bot.send_message(msg.from_user.id, "Извините, произошла ошибка, врачей данной специальности не было найдено")
    else:
        reply_message = "Список докторов: "
        for i, item in enumerate(result):
            reply_message += f'{item[0]} {item[1]} {item[2]} {item[3]}  \n'
        await bot.send_message(msg.from_user.id, reply_message)