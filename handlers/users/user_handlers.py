from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from keyboards.inline.start import startup_kb
from states.create_state import CreateState

from loader import dp, db_worker
from utils.db_api.db_sqlite_functions import Aiosqlite_worker


@dp.callback_query_handlers(Text(startswith='create_checkboxer'))
async def start_create_checkboxer(call: CallbackQuery):
    await call.answer(f'Напишите название чекбоксера!')
    await CreateState.create_checkboxer.set()

@dp.message_handler(state=CreateState.create_checkboxer)
async def start_create_checkboxer(message: Message):
    await db_worker.add_new_checkboxer(message.text)
    await message.answer(f'Создан новый чекбоксер!', reply_markup=startup_kb)

