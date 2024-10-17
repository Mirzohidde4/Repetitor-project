import asyncio, logging, calendar
from aiogram import Bot, Dispatcher, F, html
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ChatInviteLink, FSInputFile
from aiogram.filters import CommandStart, Command, and_f
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from buttons import Telefon, CreateInline, Otkazish, GetCheckbox, checkbox_options, Region, regions, variants
from dt_baza import (ReadDb, OylikStatus, UpdateOylik, ReadUserStatus, DeleteOylik, PeopleTable, DeletePeople, 
    UpdatePeople, IsFamiliy, TelefonCheck, BirthCheck)
from datetime import datetime, timedelta
from states import Info, Pay


AdminDb = ReadDb('main_admin')[0]
CardTable = ReadDb('main_card')[0]
logging.basicConfig(level=logging.INFO)
bot = Bot(token=AdminDb[4], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def EslatmaXabarYuborish(user_id, name, group, action): # vaxtlar togirlash
    if ReadDb('main_oylik'):
        for i in ReadDb('main_oylik'):
            if i[2] == int(user_id) and i[8] == int(group):
                malumot = i[6]
    
    if any((user[2] == int(user_id) and user[8] == int(group)) for user in ReadDb('main_oylik')):
        if (int(malumot) == 0) and (action == False):
            son = 1
            while not ReadUserStatus(user_id, group): 
                if son <= 3:
                    await bot.send_message(user_id, text="Siz hali to'lovni amalga oshirmadingiz. Iltimos, to'lov qiling!",
                        reply_markup=CreateInline({"💵 To'lov qilish": f"tolov_qilish_{name}_{group}"}, just=1))
                else:
                    try:
                        DeleteOylik(int(user_id), int(group))
                        DeletePeople(int(user_id), int(group))
                        await bot.send_message(int(user_id), "To'lov qilmaganingiz uchun ma'lumotlaringiz bekor qilindi.")
                    except Exception as e:
                        print(f"User ochirishda xatolik: {e}")
                    break
                son += 1       
                await asyncio.sleep(30)
        
        elif (int(malumot) == 1) and (action == True):
            today = datetime.now()
            if today.day == 17:
                if ReadDb('main_oylik'):
                    for member in ReadDb('main_oylik'):
                        if (member[2] == int(user_id)) and (member[8] == int(group)): 
                            # oy = datetime.now().month
                            oy = 11 #! vaxtincha
                            if member[5] >= 29: 
                                if (member[7] == 12) and (oy == 2):
                                    try:
                                        UpdateOylik('status', False, member[2], member[8])
                                        UpdateOylik('narx', 100, member[2], member[8])
                                        UpdatePeople('monthly', "to'lamagan ❌", member[2], member[8])
                                    except Exception as e:
                                        print(f"Xatolik: {e}")
                                
                                elif (oy - member[7]) > 1:
                                    try:
                                        UpdateOylik('status', False, member[2], member[8])
                                        UpdateOylik('narx', 100, member[2], member[8])
                                        UpdatePeople('monthly', "to'lamagan ❌", member[2], member[8])
                                    except Exception as e:
                                        print(f"Xatolik: {e}")
                                else:
                                    print("Skidka")        
                            else:
                                if (member[7] == 2) and (member[5] >= 27):
                                    if (oy - member[7]) > 1:
                                        try:
                                            UpdateOylik('status', False, member[2], member[8])
                                            UpdateOylik('narx', 100, member[2], member[8])
                                            UpdatePeople('monthly', "to'lamagan ❌", member[2], member[8])
                                        except Exception as e:
                                            print(f"Xatolik: {e}")
                                    else:        
                                        print("Skidka") 

                                elif member[5] <= 5:
                                    if (oy - member[7]) == 1:
                                        try:
                                            UpdateOylik('status', False, member[2], member[8])
                                            UpdateOylik('narx', 100, member[2], member[8])
                                            UpdatePeople('monthly', "to'lamagan ❌", member[2], member[8])
                                        except Exception as e:
                                            print(f"Xatolik: {e}")  
                                    else:        
                                        print("Skidka")    

                                elif member[5] >= 21:
                                    if (oy - member[7]) == 1:
                                        try:
                                            UpdateOylik('status', False, member[2], member[8])
                                            UpdateOylik('narx', 40, member[2], member[8])
                                            UpdatePeople('monthly', "to'lamagan ❌", member[2], member[8])
                                        except Exception as e:
                                            print(f"Xatolik: {e}")
                                    else:        
                                        print("Skidka")        

                                else:
                                    if (oy - member[7]) == 1:
                                        oylik_kunlar_soni = calendar.monthrange(today.year, today.month)[1]
                                        kunlar_soni = oylik_kunlar_soni - member[5] + 3
                                        narx = (100 * kunlar_soni) / oylik_kunlar_soni
                                        try:
                                            UpdateOylik('status', False, member[2], member[8])
                                            UpdateOylik('narx', int(narx), member[2], member[8])
                                            UpdatePeople('monthly', "to'lamagan ❌", member[2], member[8])
                                        except Exception as e:
                                            print(f"Xatolik: {e}") 
                                    else:        
                                        print("Skidka")          

                soni = 1
                while not ReadUserStatus(member[2], member[8]):
                    if soni <= 3:
                        await bot.send_message(chat_id=member[2], text="Oylik to'lovni amalga oshiring", 
                            reply_markup=CreateInline({"💵 To'lov qilish": f"tolov_qilish_{member[1]}_{member[8]}"}, just=1))
                    else:
                        try:
                            DeleteOylik(member[2], member[8])
                            DeletePeople(member[2], member[8])
                        except Exception as e:
                            print(f"User ochirishda xatolik: {e}")

                        user_status = await bot.get_chat_member(member[8], member[2])
                        if user_status.status not in ['creator', 'administrator']:
                            try:
                                await bot.ban_chat_member(member[8], member[2])
                                await bot.send_message(member[2], text="To'lovni amalga oshirmaganingiz uchun siz gurugdan chetlatildingiz.") 
                            except Exception as e:
                                print(f"user chiqarishda xatolik: {e}")        
                        else:
                            print(user_status.status, type(user_status.status))   
                        break  
                    soni += 1       
                    await asyncio.sleep(30) 
    else:
        print("Foydalanuvchi topilmadi")                              


@dp.message(CommandStart())
async def Start(message: Message, state: FSMContext):
    await state.clear()   
    if message.from_user.id == AdminDb[1]:
        await message.answer(text="Teskor start buyruqlar:")
        for i in ReadDb('main_gruppa'):
            bot_info = await bot.get_me()
            bot_username = bot_info.username
            link = f"https://t.me/{bot_username}?start={i[2]}"
            await message.answer(text=f"{i[1]}: {link}")
    
    else:
        referal = message.text.split()[1:]
        if referal:
            await state.update_data({'group': referal[0]})
            user_id = message.from_user.id
            fulname = message.from_user.full_name
            job = True
            try:
                response = int(referal[0])
                if ReadDb('main_oylik'):
                    for i in ReadDb('main_oylik'):
                        if (i[2] == int(user_id)) and (i[3] == response):
                            await message.answer(text="😊 <b>Assalomu alaykum <b>Jalol Boltaevning</b> botiga xush kelibsiz.</b>")
                            job = False
                        break
            except Exception as e:
                print("User qidirishda xatolik: ", e)    

            if job:
                await message.answer(
                    text=f"""
                        Assalomu alaykum, hurmatli <b>{fulname}</b>. Jalol Boltayevning onlayn kursida o'qimoqchimisiz? Men ustoz Jalol Boltayevning yordamchi botiman! 😎🤖
Ism-familiya, telefon raqami kabi ba'zi ma'lumotlaringizni yozib olishim kerak. Bu juda qisqa vaqt oladi. Keyin sizga yopiq guruhning havolasini yuboraman.
                    """)
                await asyncio.sleep(0.2)
                await message.answer(
                    text="""
                        Demak, boshladik.
Iltimos, familiya-ismingizni yozing (diqqat! dastlab familiya, keyin ismingizni yozing. Masalan, Boltayev Jalol).
                    """)
                dt = datetime.now()
                date = dt.strftime("%d-%m-%Y")
                await state.update_data({'date': date})
                await state.set_state(Info.name)
        else:
            await message.answer(text="😊 <b>Assalomu alaykum <b>Jalol Boltaevning</b> botiga xush kelibsiz.</b>")


@dp.message(Info.name)
async def Name(message: Message, state: FSMContext):
    if message.text:
        txt = message.text
        if IsFamiliy(txt):
            await state.update_data({'name': message.text})
            await message.answer(text="Telefon raqamingizni “<b>kontaktni yuborish</b>” (отправить контакт) tugmasi orqali yuboring.", reply_markup=Telefon)
            await state.set_state(Info.phone)
        else:
            await message.answer(text="Iltimos, birinchi familiyangizni, so'ng ismingizni yozing. Masalan, <b>Boltayev Jalol</b>.")    
    else:
        await message.answer(text="Iltimos, birinchi familiyangizni, so'ng ismingizni yozing. Masalan, <b>Boltayev Jalol</b>.")  
        

@dp.message(Info.phone)
async def Phone(message: Message, state: FSMContext):
    if message.contact:
        if message.contact.phone_number:
            await state.update_data({'phone': message.contact.phone_number})
            await message.answer(text="Sizda qo'shimcha telefon raqami bormi? Bor bo'lsa, 972990066 ko'rinishda yozib yuboring. Agar qo'shimcha raqam mavjud bo'lmasa, “<b>o'tkazib yuborish</b>” tugmasini bosing.",
                reply_markup=Otkazish)
            await state.set_state(Info.second_phone)
        else:
            await message.answer(text="Telefon raqamingizni “<b>kontaktni yuborish</b>” (отправить контакт) tugmasi orqali yuboring.", reply_markup=Telefon)
    else:
        await message.answer(text="Telefon raqamingizni “<b>kontaktni yuborish</b>” (отправить контакт) tugmasi orqali yuboring.", reply_markup=Telefon)


@dp.message(Info.second_phone)
async def QoshimchaRaqam(message: Message, state: FSMContext):
    txt = message.text
    if TelefonCheck(txt) or txt == "o'tkazib yuborish":
        await state.update_data({'second_phone': txt})
        send = await message.answer(text="Qaysi toifadansiz.",reply_markup=ReplyKeyboardRemove())
        await state.update_data({'send': send.message_id})
        await message.answer(text="Bir yoki birdan ortiq variantni tanlashingiz ham mumkin!", reply_markup=GetCheckbox(checkbox_options))
        await state.set_state(Info.kasb)
    else:
        await message.answer(
            text="Telefon raqamingizni 972990066 ko'rinishda yozib yuboring. Agar qo'shimcha raqam mavjud bo'lmasa, “<b>o'tkazib yuborish</b>” tugmasini bosing.",
            reply_markup=Otkazish)    


@dp.callback_query(lambda c: c.data in checkbox_options)
async def EditBtn(call: CallbackQuery):
    checkbox_options[call.data] = not checkbox_options[call.data]
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=GetCheckbox(checkbox_options))


@dp.callback_query(F.data == "submit", Info.kasb)
async def SubmitBtn(call: CallbackQuery, state: FSMContext):
    selected_options = [option for option, is_selected in checkbox_options.items() if is_selected]
    if selected_options:
        await call.message.delete()
        data = await state.get_data()
        send = data.get("send")
        chat_id = call.message.chat.id
        await bot.delete_message(chat_id=chat_id, message_id=send)

        await state.update_data({'kasb': ', '.join(selected_options)})
        await call.message.answer(text="Tug'ilgan sanangizni namuna bo'yicha yozing.\n<b>29.07.1998</b>")
        await state.set_state(Info.birthday)
        for ch in checkbox_options:
            checkbox_options[ch] = False            
    else:
        await call.answer(text="Qaysi toifadansiz, tanlang!")    


@dp.message(Info.birthday)
async def Birthday(message: Message, state: FSMContext):
    if message.text:
        action = message.text
        if BirthCheck(action):
            await state.update_data({'t_sana': action})
            await message.answer(text=" Yashash hududingizni belgilang.", reply_markup=Region())
            await state.set_state(Info.region)
        else:
            await message.answer(text="Tug'ilgan sanangizni namuna bo'yicha yozing.\n<b>29.07.1998</b>")    
    else:
        await message.answer(text="Tug'ilgan sanangizni namuna bo'yicha yozing.\n<b>29.07.1998</b>")


@dp.callback_query(lambda c: c.data in regions, Info.region)
async def Viloyat(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data({'hudud': call.data})
    await call.message.answer(
        text="Sizga Jalol Boltayevning onlayn kursida nima uchun qatnashyapsiz? Bir yoki birdan ortiq variantni tanlashingiz ham mumkin!",
        reply_markup=GetCheckbox(variants))
    await state.set_state(Info.maqsad)


@dp.callback_query(lambda c: c.data in variants)
async def EditButton(call: CallbackQuery):
    variants[call.data] = not variants[call.data]
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=GetCheckbox(variants))


@dp.callback_query(F.data == "submit", Info.maqsad)
async def Maqsad(call: CallbackQuery, state: FSMContext):
    selected_options = [option for option, is_selected in variants.items() if is_selected]
    
    if selected_options:
        await call.message.delete()
        maqsad = ', '.join(selected_options)
        data = await state.get_data()
        group = data.get('group')
        sanastart = data.get('date')
        name = data.get('name')
        telefon = data.get('phone')
        qosh_telefon = data.get('second_phone')
        q_telefon = (None if qosh_telefon == "o'tkazib yuborish" else qosh_telefon)
        kasb = data.get('kasb')
        tn_sana = data.get('t_sana')
        hudud = data.get('hudud')
        user_id = call.message.chat.id
        username = (f"@{call.message.chat.username}" if call.message.chat.username else None)
        this_year = datetime.now()
        usersana = str(tn_sana).split('.')[2]
        current_month = datetime.now().month
        yosh = f"{this_year.year - int(usersana)}"
        grupa = next((gr[1] for gr in ReadDb('main_gruppa') if gr[2] == int(group)), None)
        
        try:
            PeopleTable(user_id, username, name, telefon, grupa, group, sanastart, kasb, tn_sana, hudud, q_telefon, yosh, maqsad, "to'lamagan ❌")
        except Exception as e:
            print(f"Tablega yuborishda xatolik: {e}")
        
        for ch in variants:
            variants[ch] = False
        
        act = True
        if ReadDb('main_oylik'):
            if any((human[2] == int(user_id) and human[8] == int(group)) for human in ReadDb('main_oylik')):
                print('Already exits')
                act = False
        if act:    
            try:
                OylikStatus(name, user_id, int(group), AdminDb[3], 0, 0, current_month, 0)
            except Exception as e:
                print(f"Bazaga qoshishda xatolik: {e}")

        await call.message.answer(text="Ma'lumotlaringiz qabul qilindi.\nEndi to'lovni amalga oshiring.",
            reply_markup=CreateInline({"💵 To'lov qilish": f"tolov_qilish_{name}_{int(group)}"}, just=1))
        await state.set_state(Info.tolov)
        await asyncio.sleep(30)
        if any((user[8] == int(group) and (user[2] == user_id)) for user in ReadDb('main_oylik')):
            asyncio.create_task(EslatmaXabarYuborish(user_id, name, int(group), False))
        else:
            print("Gruppa IDsi topilmadi")
    else:
        await call.answer(text="variantlardan birini tanlang")
    

@dp.callback_query(F.data.startswith('tolov_'))
async def Tolov(call: CallbackQuery, state: FSMContext):
    action = call.data.split('_')[1]
    user = call.data.split('_')[2]
    gr = call.data.split('_')[3]
    user_id = call.message.chat.id
    await state.update_data({'userpay': user, 'sheetgroup': gr})

    if action == 'qilish':
        if ReadDb('main_oylik'):
            for member in ReadDb('main_oylik'):
                if (member[2] == user_id) and (member[8] == int(gr)):
                    if member[3] == 0:
                        await call.message.answer_photo(photo=FSInputFile(f"../{CardTable[1]}"), 
                            caption=f"{CardTable[3]}: {CardTable[2]}\n\nTo'lovni amalga oshirib, chekini yuboring! (skrinshot yuborsangiz ham bo'ladi). Kurs narxi <b>{member[4]} 000</b> so'm.")
                        await state.set_state(Pay.screen)
                    else:
                        await call.message.answer(text="Siz bu oy uchun to'lov qilgansiz.")
                    return           
            await call.message.answer(text="Siz ro'yxatdan o'tmagansiz.")
        else:
            await call.message.answer(text="Siz ro'yxatdan o'tmagansiz.")


@dp.message(Pay.screen)
async def Screenshot(message: Message, state: FSMContext):
    data = await state.get_data()
    user = data.get('userpay')
    sheetgroup = data.get('sheetgroup')
    user_id = message.from_user.id
    today = datetime.now()

    if message.photo:
        if ReadDb('main_oylik'):
            for member in ReadDb('main_oylik'):
                if (member[2] == user_id) and (member[8] == int(sheetgroup)):
                    sendpay = await message.answer(text="Rahmat! To'lovingiz Jalol Boltayevga yuborildi. Jalol Boltayev to'lovni tasdiqlagach, sizga guruh linkini yuboraman! Havotir olmang! To'lovingiz tez orada tasdiqlanadi (bu 10 daqiqadan 6 soatgacha vaqt olishi mumkin. Jalol ustoz ishda bo'lsalar kechroq tasdiqlab yuboradi).")
                    await bot.send_photo(
                        chat_id=AdminDb[1], photo=message.photo[-1].file_id, caption=f"<b>{user}</b> kurs to'lovini amalga oshirdi.\nQabul qilasizmi?",
                        reply_markup=CreateInline({"✅ Ha": f'qabul_xa_{user_id}_{sheetgroup}_{sendpay.message_id}_{today.day}', "❌ Yo'q": f'qabul_yoq_{user_id}_{sheetgroup}_{sendpay.message_id}_{today.day}'}, just=2))
        else:
            await message.answer(text="Siz ro'yhatdan o'tmagansiz.")    
    
    elif message.document:
        if message.document.mime_type in ("application/pdf", "image/jpeg", "image/png"):        
            if ReadDb('main_oylik'): 
                for member in ReadDb('main_oylik'):
                    if (member[2] == user_id) and (member[8] == int(sheetgroup)):
                        sendpay = await message.answer(text="Rahmat! To'lovingiz Jalol Boltayevga yuborildi. Jalol Boltayev to'lovni tasdiqlagach, sizga guruh linkini yuboraman! Havotir olmang! To'lovingiz tez orada tasdiqlanadi (bu 10 daqiqadan 6 soatgacha vaqt olishi mumkin. Jalol ustoz ishda bo'lsalar kechroq tasdiqlab yuboradi).")
                        await bot.send_document(chat_id=AdminDb[1], document=f"{message.document.file_id}", caption=f"<b>{user}</b> kurs to'lovini amalga oshirdi.\nQabul qilasizmi?",
                            reply_markup=CreateInline({"✅ Ha": f'qabul_xa_{user_id}_{sheetgroup}_{sendpay.message_id}_{today.day}', "❌ Yo'q": f'qabul_yoq_{user_id}_{sheetgroup}_{sendpay.message_id}_{today.day}'}, just=2))
    else:
        await message.answer_photo(photo=CardTable[1],caption=f"{CardTable[3]}: {CardTable[2]}\n\nTo'lovni amalga oshirib screenshotini yuboring.")
        await state.set_state(Pay.screen)    


@dp.callback_query(F.data.startswith('qabul_')) 
async def Accept(call: CallbackQuery, state: FSMContext):
    action = call.data.split('_')[1]
    user_id = call.data.split('_')[2]
    sheetgroup = call.data.split('_')[3]
    sendpay = call.data.split('_')[4]
    sana = call.data.split('_')[5]
    await call.message.delete()

    if action == "xa":
        await bot.delete_message(chat_id=user_id, message_id=sendpay)        
        for member in ReadDb('main_oylik'):
            if (member[2] == int(user_id)) and (member[8] == int(sheetgroup)):
                fullname = member[1]
                await bot.send_message(chat_id=user_id,
                    text=f"Qadrli <b>{fullname}</b>, to'lovingiz tasdiqlandi. Jalol Boltayev ustozga ishonchingiz uchun rahmat! Biz ham jamoamiz bilan sizning ishonchingizni oqlashga qattiq harakat qilamiz. Jalol ustoz test materiallari, ta'lim sifati, metodika bilan shug'ullanadi, to'lov masalalari bilan esa men shug'ullanaman. Har to'lov payti kelganda eslatib turaman :)")
                
                if member[6] == 0:
                    try:
                        UpdateOylik('info', 1, user_id, int(sheetgroup))
                    except Exception as e:
                        print(f"Oylik info yangilashda xatolik: {str(e)}")  
                    
                    try:
                        # expire_date = timedelta(minutes=5)
                        invite_link: ChatInviteLink = await bot.create_chat_invite_link(chat_id=int(sheetgroup), expire_date=None, member_limit=1)
                        await bot.send_message(chat_id=user_id, text=f"➕ <b>Guruhga qo'shilishingiz mumkin.</b>\n\n{invite_link.invite_link}")

                    except Exception as e:
                        print(f"Havola yaratishda xatolik: {str(e)}")  
                try:        
                    UpdateOylik('status', 1, user_id, int(sheetgroup))
                    UpdatePeople('monthly', "to'lagan ✅", user_id, int(sheetgroup))
                    UpdateOylik('date', int(sana), user_id, int(sheetgroup))
                except Exception as e:
                    print(f"Oylik status yangilashda xatolik: {str(e)}")  
                break
            else:
                print("User topilmadi")                 
    
    elif action == "yoq":
        await bot.delete_message(chat_id=user_id, message_id=sendpay)
        await bot.send_message(chat_id=user_id, text="🚫 To'lovingiz qabul qilinmadi.")
    await state.clear()


@dp.message(F.new_chat_members) 
async def NewMember(message: Message):
    new_members = message.new_chat_members
    group = message.chat.id
    
    for member in new_members:
        await message.delete()
        user_id = member.id
        action = True
        if ReadDb('main_oylik'):
            for user in ReadDb('main_oylik'):
                if (user[2] == user_id) and (user[8] == group): 
                    action = False

        if action:  
            user_status = await bot.get_chat_member(group, user_id)
            if user_status.status not in ['creator', 'administrator']:
                try:
                    await bot.ban_chat_member(group, user_id)
                except Exception as e:
                    print(f"user chiqarishda xatolik: {e}")        
            else:
                print(user_status.status)


@dp.message(F.left_chat_member) 
async def LeftMember(message: Message):
    if message.left_chat_member:
        user_id = message.left_chat_member.id
        user_url = message.left_chat_member.url
        group_id = message.chat.id
        response = next((gr[1] for gr in ReadDb('main_gruppa') if gr[2] == int(group_id)), None)
        if ReadDb('main_oylik'):
            for user in ReadDb('main_oylik'):
                if (user[2] == user_id) and (user[8] == group_id):
                    await bot.send_message(chat_id=AdminDb[1], text=f"Foydalanuvchi <a href='{user_url}'><b>{user[1]}</b></a> {response}-guruhni tark etdi. Ma'lumotlarini tozalaymi?",
                    reply_markup=CreateInline({"✅ Xa": f"tozalash_xa_{user_id}_{group_id}", "❌ Yo'q": f"tozalash_yoq_{user_id}_{group_id}"}, just=2))
        await message.delete()


@dp.callback_query(F.data.startswith('tozalash_'))
async def Tozalash(call: CallbackQuery):
    action = call.data.split('_')[1]
    user_id = call.data.split('_')[2]
    group = call.data.split('_')[3]

    if action == 'xa':
        await call.message.delete()
        try:
            DeleteOylik(int(user_id), int(group))
            DeletePeople(int(user_id), int(group))
            print("Ma'lumot muvaffaqiyatli o'chirildi")
        except Exception as e:
            print(f"User ochirishda xatolik: {e}")
        await call.message.delete()
    
    elif action == 'yoq':
        await call.message.delete()
        try:
            # expire_date = timedelta(minutes=5)
            invite_link: ChatInviteLink = await bot.create_chat_invite_link(chat_id=int(group), expire_date=None, member_limit=1)
            await bot.send_message(chat_id=user_id, text=f"➕ <b>Siz guruhni tark etdingiz, havola orqali qayta qo'shilishingiz mumkin.</b>\n\n{invite_link.invite_link}")
        except Exception as e:
            print(f"Havola yaratishda xatolik: {str(e)}") 


async def send_message_to_users():
    while True:
        if ReadDb('main_oylik'):
            for member in ReadDb('main_oylik'):
                if member[6] == 1:
                    await EslatmaXabarYuborish(member[2], member[1], member[8], True)
        await asyncio.sleep(60)        


@dp.startup()
async def on_startup():
    asyncio.create_task(send_message_to_users())


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Bot o`chdi: {e}")


    









    # data = await state.get_data()
    # name = data.get('name')
    # telefon = data.get('phone')
    # qosh_telefon = data.get('second_phone')
    # q_telefon = (None if qosh_telefon == "o'tkazib yuborish" else qosh_telefon)
    # kasb = data.get('kasb')
    # t_sana = data.get('t_sana')
    
    # txt = f"<b>Ism-familiya:</b> {name}\n<b>Telefon:</b> {telefon} {f'({q_telefon})' if q_telefon else ''}\n<b>Toifa</b>: {kasb}\n<b>Tug'ilgan sana:</b> {t_sana}\n<b>Yashash hududi:</b> {call.data}"

    # await call.message.answer(
    #     text=f"{txt}\n\n<b>Ro'yxatdan o'tishga rozimisiz?</b>",
    #     reply_markup=CreateInline({'✅ Xa': 'tasdiqlash_xa', "❌ Yo'q": 'tasdiqlash_yoq'}, just=2)
    # )
    # await state.set_state(Info.tasdiq)


# @dp.callback_query(F.data.startswith('tasdiqlash_'), Info.tasdiq)
# async def UserAnswer(call: CallbackQuery, state: FSMContext):
#     await call.message.delete()
#     action = call.data.split("_")[1]
    
#     if action == 'xa':
#         data = await state.get_data()
#         group = data.get('group')
#         sanastart = data.get('date')
#         name = data.get('name')
#         telefon = data.get('phone')
#         qosh_telefon = data.get('second_phone')
#         q_telefon = (None if qosh_telefon == "o'tkazib yuborish" else qosh_telefon)
#         kasb = data.get('kasb')
#         tn_sana = data.get('t_sana')
#         hudud = data.get('hudud')
#         user_id = call.message.chat.id
#         username = (f"@{call.message.chat.username}" if call.message.chat.username else None)
        
#         api_id = (AdminDb[3] if group == '1' else AdminDb[4] if group == '2' else AdminDb[5] if group == '3' else None)
#         if Read_User(api_id):
#             id = int(Read_User(api_id)) + 1
#         else:
#             id = 1

#         print(sanastart, type(sanastart), tn_sana, type(tn_sana))
#         data_to_send = {
#             'id': id,
#             'telegram id': user_id,
#             'username': username,
#             'ism-familiya': name,
#             'telefon': telefon,
#             'start bot': sanastart,
#             'toifa': kasb,
#             'tug`ilgan sana': tn_sana,
#             'yashash hududi': hudud,
#             "qo'shimcha telefon": q_telefon,
#             'oylik': "to'lanmagan ❌"
#         }

#         act = True
#         if ReadDb('Oylik'):
#             if any((human[1] == int(user_id) and human[2] == int(group)) for human in ReadDb('Oylik')):
#                 print('Already exits')
#                 act = False

#         if act:    
#             try:
#                 OylikStatus(name, user_id, group, False)
#             except Exception as e:
#                 print(f"Bazaga qoshishda xatolik: {e}")

#         id = None
#         if group == '1':
#             id = AdminDb[6]
#             response = requests.post(AdminDb[3], json={"data": [data_to_send]})
#         elif group == '2':    
#             id = AdminDb[7]
#             response = requests.post(AdminDb[4], json={"data": [data_to_send]})
#         elif group == '3':
#             id = AdminDb[8]
#             response = requests.post(AdminDb[5], json={"data": [data_to_send]}) 

#         if str(response.status_code) == '201':
#             await call.message.answer(text="<b>Ma'lumotlaringiz qabul qilindi.</b>")
#             await state.clear()    
#         else:    
#             await call.message.answer(text="<b>Ma'lumotlaringiz qabul qilinmadi.</b>")

#     elif action == 'yoq':
#         await state.clear()
#         await call.message.answer(text="⛔️ <b>Ma'lumotlaringiz bekor qilindi.</b>")                    
              