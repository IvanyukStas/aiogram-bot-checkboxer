from aiogram import types


def checkbox_kb(checkbox, id):
    checkbox_button = []
    for i in checkbox:
        chbox_name = i[1]
        checkbox_button.append(types.InlineKeyboardButton(chbox_name, callback_data='checkbox_id_' + str(i[0])))
    checkbox_button.append(types.InlineKeyboardButton('Добавить чекбокс', callback_data='checkboxer_id' + str(id)))
    chboxer_kb = types.InlineKeyboardMarkup(row_width=1)
    chboxer_kb.add(*checkbox_button)
    return chboxer_kb


async def show_checkboxes_kb(id, state):
    await state.finish()
    checkbox_button = [types.InlineKeyboardButton('Показать чекбоксы', callback_data=f'checkboxer_id_{id}')]
    checkbox_kb = types.InlineKeyboardMarkup()
    checkbox_kb.add(*checkbox_button)
    return checkbox_kb