from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.filters import Text

from keyboards.inline.checkboxers_kb import checkboxer_kb
from keyboards.inline.start import startup_kb
from loader import dp, db_worker
from states.checboxer_state import CreateState


@dp.callback_query_handler(text='create_checkboxer')
async def start_create_checkboxer(call: CallbackQuery):
    await call.message.answer(f'Напишите название чекбоксера!')
    await CreateState.create_checkboxer.set()


@dp.callback_query_handler(Text(startswith='my_checkboxers'))
async def get_checkboxers(call: CallbackQuery):
    checkboxers = await db_worker.get_checkboxers_sqlite(call.from_user.id)
    await call.message.answer(f'Ваши чекбоксеры!', reply_markup=checkboxer_kb(checkboxers))


@dp.message_handler(state=CreateState.create_checkboxer)
async def start_create_checkboxer(message: Message, state: FSMContext):
    await db_worker.add_new_checkboxer_sqlite(message.text, message.from_user.id, chboxer_status='private')
    await message.delete()
    await message.answer(f'Создан новый чекбоксер!', reply_markup=startup_kb)
    await state.finish()

