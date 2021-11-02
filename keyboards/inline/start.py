from aiogram import types

startup_buttons = [types.InlineKeyboardButton('Мои чекбоксеры', callback_data='my_checkboxers'),
    types.InlineKeyboardButton('Создать чекбоксер', callback_data='create_checkboxer')]
startup_kb = types.InlineKeyboardMarkup(row_width=2)
startup_kb.add(*startup_buttons)
