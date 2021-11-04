from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from keyboards.inline import checkboxers_kb
from keyboards.inline.checkbox_kb import checkbox_kb, show_checkboxes_kb
from keyboards.inline.checkboxers_kb import checkboxer_kb
from keyboards.inline.start import startup_kb
from states.checboxer_state import CreateState

from loader import dp, db_worker
from utils.db_api.db_sqlite_functions import Aiosqlite_worker



@dp.callback_query_handler(text='create_checkboxer')
async def start_create_checkboxer(call: CallbackQuery):
    await call.message.answer(f'Напишите название чекбоксера!')
    await CreateState.create_checkboxer.set()


@dp.callback_query_handler(Text(startswith='my_checkboxers'))
async def get_checkboxers(call: CallbackQuery):
    checkboxers = await db_worker.get_checkboxers(call.from_user.id)
    await call.message.answer(f'Ваши чекбоксеры!', reply_markup=checkboxer_kb(checkboxers))


@dp.callback_query_handler(Text(startswith='checkboxer_id'))
async def get_checkboxes(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    checkboxes = await db_worker.get_checkboxes(data[-1])
    await state.update_data(checkboxer_id=data[-1])
    await CreateState.create_checkbox.set()
    if checkboxes == False:
        await call.message.answer('У вас пока нет чекбоксов. '
                                  'Напишите в чат название чекбокса и мы его добавим')
    else:
        await call.message.answer(f'Ваши чекбоксы!', reply_markup=checkbox_kb(checkboxes, data[-1]))


@dp.message_handler(state=CreateState.create_checkbox)
async def add_checkbox(message: Message, state: FSMContext):
    data = await state.get_data()
    await db_worker.add_new_checkbox(message.text, data['checkboxer_id'])
    await message.answer(f'Наберите название нового чекбоксера или нажмите,\n '
                              f'чтоб получить список чебоксов!',
                         reply_markup=show_checkboxes_kb(data['checkboxer_id']))


@dp.callback_query_handler(Text(startswith='checkboxer_id'), state=CreateState.create_checkbox)
async def get_checkboxes_in_state(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    checkboxes = await db_worker.get_checkboxes(data['checkboxer_id'])
    await call.message.answer(f'Ваши чекбоксы!', reply_markup=checkbox_kb(checkboxes, data['checkboxer_id']))


@dp.message_handler(state=CreateState.create_checkboxer)
async def start_create_checkboxer(message: Message, state: FSMContext):
    await db_worker.add_new_checkboxer(message.text, message.from_user.id, chboxer_status='private')
    await message.answer(f'Создан новый чекбоксер!', reply_markup=startup_kb)
    await state.finish()




