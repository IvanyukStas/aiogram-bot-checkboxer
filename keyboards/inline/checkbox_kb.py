from aiogram import types

create_checkbox_kb = types.InlineKeyboardMarkup()
create_checkbox_kb.add(types.InlineKeyboardButton('Добавить чекбокс!', callback_data='create_checkbox'))

def checkbox_kb(checkbox, id):
    checkbox_button = []
    for i in checkbox:
        chbox_name = i[1]
        if i[2] == '0':
            check_status = '❌'
        else:
            check_status = '✅'
        checkbox_button.append(types.InlineKeyboardButton(check_status+chbox_name, callback_data='update_' + str(i[2])
                                                                                                 + '_' + str(i[0])))
    a = types.InlineKeyboardButton('Добавить чекбокс', callback_data='create_checkbox')
    b = types.InlineKeyboardButton('Начало', callback_data='begin_of_game')
    chboxer_kb = types.InlineKeyboardMarkup(row_width=1)
    chboxer_kb.add(*checkbox_button)
    chboxer_kb.row(a, b)
    return chboxer_kb


def show_checkboxes_kb(id):
    checkbox_button = [types.InlineKeyboardButton('Показать чекбоксы', callback_data=f'checkboxer_id_{id}')]
    checkbox_kb = types.InlineKeyboardMarkup()
    checkbox_kb.add(*checkbox_button)
    return checkbox_kb