from aiogram import types



def checkboxer_kb(checkboxers):
    checkboxer_button = []
    for i in checkboxers:
        chboxer_name = i[1]
        checkboxer_button.append(types.InlineKeyboardButton(chboxer_name, callback_data='checkboxer_id_'+str(i[0])))
    chboxer_kb = types.InlineKeyboardMarkup(row_width=1)
    chboxer_kb.add(*checkboxer_button)
    return chboxer_kb