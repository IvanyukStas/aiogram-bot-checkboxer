import logging
import os.path

from aiogram import executor

from loader import dp, db_worker
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    if not os.path.exists(db_worker.db_name):
        await db_worker.create_database_sqlite()



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

