from aiogram.fsm.state import State, StatesGroup


class Info(StatesGroup):
    name = State()
    phone = State()
    second_phone = State()
    kasb = State()
    birthday = State()
    region = State()
    tasdiq = State()
    maqsad = State()
    tolov = State()


class Pay(StatesGroup):
    screen = State()
