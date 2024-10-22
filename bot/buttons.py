from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from dt_baza import ReadDb


def Createreply(*args, contact=False, just=int) -> ReplyKeyboardBuilder:
    bulder = ReplyKeyboardBuilder()
    for i in args:
        bulder.add(KeyboardButton(text=i, request_contact=True if contact else False))
    bulder.adjust(just)
    return bulder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def CreateInline(*button_rows, just=int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for row in button_rows:
        for text, callback_data in row.items():
            if callback_data.startswith('https:'):
                builder.add(InlineKeyboardButton(text=text,url=callback_data))
            else:
                builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    builder.adjust(just)
    return builder.as_markup()


checkbox_options = {}
id = next((i[0] for i in ReadDb('main_botmessage') if i[1] == 'toifa'), None)
for a in ReadDb('main_botbuttoninlyne'):
    if a[3] == id:
        checkbox_options[a[1]] = False


variants = {}
mid = next((f[0] for f in ReadDb('main_botmessage') if f[1] == 'goal'), None)
for d in ReadDb('main_botbuttoninlyne'):
    if d[3] == mid:
        variants[d[1]] = False


def GetCheckbox(dictname: dict):
    keyboard = InlineKeyboardBuilder()
    for option, is_selected in dictname.items():
        text = f"{option} {'☑️' if is_selected else ''}"
        keyboard.add(InlineKeyboardButton(text=text, callback_data=option))
    keyboard.add(InlineKeyboardButton(text="✅ Yuborish", callback_data="submit"))
    keyboard.adjust(2)
    return keyboard.as_markup()


regions = ["Toshkent", "Andijon", "Buhoro", "Farg'ona", "Jizzax", "Xorazm", "Namangan", "Navoiy", "Qashqadaryo", "Qoraqalpog'iston R.", "Samarqand", "Sirdayo", "Surxondaryo", "Toshkent sh."]
def Region() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for r in regions:
        builder.add(InlineKeyboardButton(text=r, callback_data=r))
    builder.adjust(2)    
    return builder.as_markup()