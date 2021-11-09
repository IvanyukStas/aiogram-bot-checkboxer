import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.webhook import DeleteMessage
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageToDeleteNotFound

from keyboards.inline.checkbox_kb import checkbox_kb, show_checkboxes_kb, create_checkbox_kb
from keyboards.inline.start import startup_kb
from loader import dp, db_worker, bot
from aiogram.dispatcher.filters import Text

from states.checboxer_state import CreateState


@dp.callback_query_handler(Text(startswith='checkboxer_id'))
async def get_checkboxes(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    checkboxes = await db_worker.get_checkboxes(data[-1])
    await state.update_data(checkboxer_id=data[-1])
    logging.info('Добавили стетйт криате')
    if checkboxes == False:
        await call.message.delete()
        await call.message.answer('У вас пока нет чекбоксов. ', reply_markup=create_checkbox_kb)
        await CreateState.create_checkbox.set()
    else:
        await call.message.delete()
        await call.message.answer(f'Ваши чекбоксы!', reply_markup=checkbox_kb(checkboxes, data[-1]))
        await CreateState.create_checkbox.set()
        logging.info(' используем get_checkboxes')

@dp.message_handler(state=CreateState.create_checkbox)
async def  add_chechbox_message_handl(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    if not message.text == []:
        await db_worker.add_new_checkbox(message.text, data['checkboxer_id'])
    if 'message_id' in data:
        await bot.delete_message(data['chat_id'], data['message_id'])
        logging.info(f'Удалили сообщение {data["message_id"]}')
    await state.update_data(message_id=message.message_id, chat_id=message.chat.id)
    await message.answer(f'Наберите название нового чекбоксера или нажмите,\n '
                              f'чтоб получить список чебоксов!',
                              reply_markup=show_checkboxes_kb(data['checkboxer_id']))


@dp.callback_query_handler(text='create_checkbox', state=CreateState.create_checkbox)
async def add_checkbox(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if 'message_id' in data:
        try:
            await bot.delete_message(data['chat_id'], data['message_id'])
            logging.info(f'Удалили сообщение {data["message_id"]}')
        except MessageToDeleteNotFound:
            pass
    await state.update_data(message_id=call.message.message_id, chat_id=call.message.chat.id)
    if not call.message.text == []:
        await db_worker.add_new_checkbox(call.message.text, data['checkboxer_id'])
    await call.message.answer(f'Наберите название нового чекбоксера или нажмите,\n '
                              f'чтоб получить список чебоксов!',
                      reply_markup=show_checkboxes_kb(data['checkboxer_id']))



@dp.callback_query_handler(Text(startswith='checkboxer_id'), state=CreateState.create_checkbox)
async def get_checkboxes_in_state(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    checkboxes = await db_worker.get_checkboxes(data['checkboxer_id'])
    await call.message.delete()
    await call.message.answer(f'Ваши чекбоксы!', reply_markup=checkbox_kb(checkboxes, data['checkboxer_id']))
    logging.info(' используем get_checkboxes_in_state')


@dp.callback_query_handler(Text(startswith='update'), state=CreateState.create_checkbox)
async def update_checkbox(call: CallbackQuery, state: FSMContext):
    data_id = call.data.split('_')[-1]
    data_status = call.data.split('_')[-2]
    if data_status == '0':
        await db_worker.update_checkbox(data_id, 1)
    else:
        await db_worker.update_checkbox(data_id, 0)
    data = await state.get_data()
    checkboxes = await db_worker.get_checkboxes(data['checkboxer_id'])
    await call.message.delete()
    await call.message.answer(f'Ваши чекбоксы!', reply_markup=checkbox_kb(checkboxes, data['checkboxer_id']))


@dp.callback_query_handler(text='begin_of_game', state='*')
async def cancel(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer('Выберите раздел', reply_markup=startup_kb)