import logging

from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.db_api.db_sqlite_functions import Aiosqlite_worker
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    a = Aiosqlite_worker()
    await a.create_database()
    await a.add_new_user('dsfdsfdsf', '342423423423423')
    await a.add_new_checkboxer('xtr,jrcth', 'public', 1)
    await a.add_new_checkbox('dsfdsfdsfds', 'dsfdsfdsfdsfdsf', 1)
    a = await a.get_user('342423423423423')
    print(a)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

