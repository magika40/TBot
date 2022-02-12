import logging
from aiogram import Bot, Dispatcher, executor, types
import os
import sys
import time
import asyncio
import conf
import sqlite3
import datetime
import re

sys.path.append(os.path.abspath("./res/"))
from res.untitled12 import construct_data

start = time.time()


def datanow(data):
    if datacheck(data) == True:
        nstr = data
        nstr = nstr[3] + nstr[4] + '-' + nstr[0] + nstr[1]
    elif data == 'now':
        nstr = datetime.datetime.now().strftime("%m-%d")
    elif data == 'tomorrow':
        now = datetime.datetime.now() + datetime.timedelta(days=1)
        nstr = now.strftime("%m-%d")
    elif data == "*":
        pika = " SELECT * FROM lessons "
        return pika
    pika = "SELECT * FROM lessons where date = '" + nstr + "' order by date asc;"
    return pika
now = datetime.datetime.now() + datetime.timedelta(days=1)
now = now.strftime("%m-%d")
sqllist = ['Дата: ', 'Время: ', 'Название: ', 'Адрес: ']

def sql_man(data):
    con = sqlite3.connect(r'res/tangodatabase.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(datanow(data))
    sqll = cur.fetchall()
    con.cursor().close()
    con.close()

    return sqll

def parslist(sqlist, ind):
    sqlstr = ''
    for kpar in range(4):
        sqlstr = sqlstr + sqllist[kpar] + sqlist[ind][kpar] + '\n'
    return sqlstr

def datacheck(data):
    match = re.search(r'\d{2}.\d{2}', data)
    #date = datetime.strptime(match.group(), '%m-%d').date()
    #print(date)
    if (match != None):
        result = True
    else:
        result = False
    return result

bot_token = conf.TOKEN_A
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)
"""
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!")
"""

"""updata = asyncio.ensure_future(update_data())

update_loop = asyncio.get_event_loop()
asyncio.set_event_loop(update_loop)
update_loop.run_until_complete(asyncio.gather(updata))
update_loop.close()"""

flaglist = [0,0,0,0,0,0]

async def print_scheduler(message: types.Message, when=''):
    srts = sql_man(when)
    for j in range(len(srts)):
        await asyncio.sleep(0.1)
        await message.reply(parslist(srts, j))

async def print_schedule(message: types.Message, when=''):
    srts = sql_man(when)
    for i in range(len(srts)):
        await asyncio.sleep(0.1)
        await message.answer(parslist(srts, i))

@dp.message_handler(commands=['update'])
async def up(message: types.Message):
    construct_data()
    await message.answer('Ok!')
#await message.reply()


@dp.message_handler(commands=['today'])
async def beka(message: types.Message):
    await print_scheduler(message, 'now')

@dp.message_handler(commands=['tomorrow'])
async def send_welcome(message: types.Message):
    await print_scheduler(message, 'tomorrow')

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons_1 = ["Сегодня", "Завтра"]
    buttons_2 = ["Напишу дату","Что есть на неделе?"]
    keyboard.add(*buttons_1)
    keyboard.add(*buttons_2)
    await message.answer("Когда пойдём на милонгу?", reply_markup=keyboard)

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("У меня лапки..")

@dp.message_handler(commands=['data'])
async def send_welcome(message: types.Message):
    await message.answer("Укажите дату в формате: 'dd.mm'")
    flaglist[0] = 0
    if (datacheck(str(message.text)) == True):
        await print_scheduler(message, message.text)

@dp.message_handler(commands=['schedule'])
async def send_welcome(message: types.Message):
    await message.answer("Расписание пока не готово")

@dp.message_handler()
async def echo(message: types.Message):
    if message.text == "Напишу дату":
        await message.answer("Укажите дату в формате: 'dd.mm'")
        flaglist[0] = 0
    elif datacheck(message.text) == True:
        await print_schedule(message, message.text)
    elif message.text == "Завтра":
        await print_schedule(message, 'tomorrow')
    elif message.text == "Сегодня":
        await print_schedule(message, 'now')
    elif message.text == "Что есть на неделе?":
        await print_scheduler(message, '*')

    elif message.text == "пидр":
        await message.answer("сам такой")
    else:
        if flaglist[0] == 1:
            await message.answer("Что-то пошло не так")
        flaglist[0] = 1


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
