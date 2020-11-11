import os
import heroku3
import gspread
import objects
import asyncio
from objects import code
from aiogram import types
from datetime import datetime
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from objects import executive as send_dev_error
from objects import async_exec as async_executive


idMe = 396978030
stamp1 = objects.time_now()
objects.environmental_files()
bot = objects.start_main_bot('async', os.environ['TOKEN'])
dispatcher = Dispatcher(bot)
# ========================================================================================================
#objects.start_message(os.environ['TOKEN'], stamp1)


@dispatcher.message_handler()
async def repeat_all_messages(message: types.Message):
    if message['chat']['id'] != idMe:
        await bot.send_message(message['chat']['id'], 'К тебе этот бот не имеет отношения, уйди пожалуйста')
    else:
        if message.text.startswith('/log'):
            doc = open('log.txt', 'rt')
            await bot.send_document(message['chat']['id'], doc, reply_markup=None)
        else:
            await bot.send_message(message['chat']['id'], 'Я работаю', reply_markup=None)


async def heroku(activate):
    worksheet = gspread.service_account('reboot1.json').open('heroku cloud').worksheet('keys')
    raw_users = worksheet.get('A1:Z50000', major_dimension='ROWS')
    if activate.lower() == 'one':
        scale_first = 1
        scale_second = 0
    else:
        scale_first = 0
        scale_second = 1
    update_users = {}
    row_id = 0
    users = {}
    for user in raw_users:
        row_id += 1
        if len(user) == 6:
            users[row_id] = user  # исключаем из массива ненужных или специально убранных акков (графа исключения)
    for row_id in users:
        user = users.get(row_id)
        for connect in [0, 3]:
            try:
                connection = heroku3.from_key(user[connect])
                if len(connection.apps()) == 1:
                    for app in connection.apps():
                        if app.name != user[connect + 1]:
                            user[connect + 1] = app.name
                            update_users[row_id] = user
                            users[row_id] = user
                        if connection.account().email != user[connect + 2]:
                            user[connect + 2] = connection.account().email
                            update_users[row_id] = user
                            users[row_id] = user
                        for process in app.process_formation():
                            if connect == 0:
                                process.scale(scale_first)
                            elif connect == 3:
                                process.scale(scale_second)
                else:
                    break
            except IndexError and Exception as error:
                error = str(error) + '\n\nTroubles:\n' + \
                    user[connect] + ' ' * 5 + user[connect + 1] + ' ' * 5 + user[connect + 2]
                send_dev_error(error)

    worksheet = gspread.service_account('reboot1.json').open('heroku cloud').worksheet('keys')
    for user_row in update_users:
        user_range = worksheet.range('A' + str(user_row) + ':F' + str(user_row))
        for i in range(0, len(update_users[user_row])):
            user_range[i].value = update_users[user_row][i]
        worksheet.update_cells(user_range)
        await asyncio.sleep(2)


async def to_second():
    while True:
        try:
            stamp = objects.time_now()
            objects.printer('проверка')
            day = int(datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%d'))
            hours = int(datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%H'))
            if day == 17 and hours == 6:
                title = 'Переходим на второй (' + code('Two') + ') сервер heroku\n'
                dev = objects.send_dev_message(title + '\n' + objects.log_time(tag=code), tag=None, good=True)
                await heroku('Two')
                objects.edit_dev_message(dev, objects.log_time(tag=code))
                await asyncio.sleep(3000)
            await asyncio.sleep(1000)
        except IndexError and Exception:
            await async_executive()


async def to_first():
    while True:
        try:
            stamp = objects.time_now()
            objects.printer('проверка')
            day = int(datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%d'))
            hours = int(datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%H'))
            if day == 1 and hours == 6:
                title = 'Переходим на первый (' + code('One') + ') сервер heroku\n'
                dev = objects.send_dev_message(title + '\n' + objects.log_time(tag=code), tag=None, good=True)
                await heroku('One')
                objects.edit_dev_message(dev, objects.log_time(tag=code))
                await asyncio.sleep(3000)
            await asyncio.sleep(1000)
        except IndexError and Exception:
            await async_executive()


if __name__ == '__main__':
    for func in [to_first, to_second]:
        dispatcher.loop.create_task(func())
    executor.start_polling(dispatcher)