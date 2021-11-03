from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateState(StatesGroup):
    create_checkboxer = State()
    create_checkbox = State()


class GetState(StatesGroup):
    get_checkboxer = State()


