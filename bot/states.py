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


class CardNumber(StatesGroup):
    photo = State()
    number = State()
    name = State()


class Pay(StatesGroup):
    screen = State()


# class Admin(StatesGroup):
#     token = State()
#     admin_id = State()
#     gruppa = State()
