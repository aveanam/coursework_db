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

@dp.message_handler(commands=['new_visit_doc'], state = '*' )
async def msg_info_new_visit(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Введите специализацию врача, к которому вы хотите записаться')
    await users_states.get_new_visit_state.set()

# Пользователь вводит название специализации: гинеколог, эндокринолог, ЛОР и т.д.
# Выведем свободные окошки у данного врача

@dp.message_handler(content_types=['text'], state= users_states.get_new_visit_state)
async def msg_info_free_time(msg: types.Message):
    db_pg_rb_obj.execute('select * from get_free_slots (%s)', [str(msg.text)])
    result = db_pg_rb_obj.fetchall()

    if not result:
        await bot.send_message(msg.from_user.id,
                               "Извините, произошла ошибка, врачей данной специальности не было найдено или в данный момент свободных окон для записей нет \n"
                               "Проверьте наличие врачей данной специальности при помощи комманды /info_doctors_spec")
        await users_states.get_doc_spec.set()
    else:
        reply_message = ""
        for i, item in enumerate(result):
            reply_message += f'{item[0]} {item[1]} {item[2]} {item[3]} {item[4]} {item[5]} \n'
        await bot.send_message(msg.from_user.id, reply_message)
        await users_states.add_new_visit_w_id_pat.set()
        await bot.send_message(msg.from_user.id, "Для записи введите код записи, подходящего вам временного слота, ФИО и ваш номер телефона, который записан в вашей медицинской карте")

# Пользователь выбирает нужный слот и отправляет в чат код записи, по которому мы его запишем
@dp.message_handler(content_types=['text'], state=users_states.add_new_visit_w_id_pat)
async def add_new_visit_to_doc(msg: types.Message):
    #await bot.send_message(msg.from_user.id, msg.text)
    code_visit, name1, name2, name3, phone_num = msg.text.split()
    name = name1 + " " + name2 + " " + name3
    print(phone_num)
    db_pg_doc_obj.execute('select * from get_id_patient (%s, %s)', [name, phone_num])
    result_tmp = db_pg_doc_obj.fetchall()

    if not result_tmp:
        await bot.send_message(msg.from_user.id, "Извините, пациента с такими данные не найдено, проверьте данные и попробуйте снова"
                                                 "\n Если у вас нет мед. карты в нашей клинике, то заведите её с помощью команды /new_med_card")
    else:
        id_pat_tmp = int(result_tmp[0][0])
        db_pg_rb_obj.execute('select add_new_patient_visit (%s, %s)', [int(code_visit), id_pat_tmp])
        result_tmp_2 = db_pg_rb_obj.fetchall()

        if not result_tmp_2:
            await bot.send_message(msg.from_user.id,
                                   "Извините, но произошла ошибка, попробуйте снова")
        else:
            await bot.send_message(msg.from_user.id,
                                   "Вы успешно записаны на приём к врачу! Ждём встречи с вами! :)")
