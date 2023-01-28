#--------------   Bot start   --------------------

import logging

from database import Database
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, ADMIN # API_Token va Adminlar idlari
from aiogram.dispatcher.filters import Text 
from buttons import *

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext 
from state import StateData, StateSearch

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database()

#--------------   Main menu   --------------------

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    data = db.select_users(message.from_user.id)
    if data:    
        await message.answer("Assalomu alekum!\nElektron kutubxonaga xush kelibsiz!", reply_markup=menu)
    else:
        tel_id = message.from_user.id
        name = message.from_user.first_name
        db.insert_users(tel_id, name)
        await message.answer("Assalomu alekum!\nElektron kutubxonaga xush kelibsiz!", reply_markup=menu)


@dp.message_handler(text="Kitoblar")
async def category(message: types.Message):
    markup = await for_category_get_all()
    await message.answer("Bo'limlardan birini tanlang!", reply_markup=markup)

@dp.callback_query_handler(Text(startswith="productall_"))
async def get_category_products(call: types.CallbackQuery):
    index = call.data.index("_")
    id = call.data[index+1:]
    products = await get_category_id(id)
    await call.message.answer("Kitoblardan birini tanlang!", reply_markup=products)

@dp.callback_query_handler(Text(startswith="products_"))
async def get_products(call: types.CallbackQuery):
    index = call.data.index("_")
    id = call.data[index+1:]
    product = db.select_product_id(id)

    await call.message.answer_photo(photo=product[5], caption=f"Siz tanlagan kitob!\n\nKitob nomi: {product[3]}\nKitob haqida: {product[4]}\n\nKitob narxi: {product[6]}")
    await call.message.answer_document(document=product[2])

#--------------   Aloqa    -----------------

@dp.message_handler(text="Aloqa")
async def admin_menu(message: types.Message):
    await message.answer("Murojaat va takliflar uchun: @T_Zafarbek_S")

#--------------   ADMIN menu    -----------------

@dp.message_handler(commands=['admin'], user_id=ADMIN)
async def admin_menu(message: types.Message):
    await message.answer("Admin menusi",reply_markup=admin)

@dp.message_handler(text="Orqaga qaytish", user_id=ADMIN)
async def admin_menu(message: types.Message):
    await message.answer("Asosiy menu",reply_markup=menu)

#--------------   Book search   -----------------

@dp.message_handler(text="Qidirish", state="*")
async def search_book(message: types.Message, state: FSMContext):
    await message.answer("Qidirish uchun kitob nomini kiriting: ")
    await state.set_state(StateSearch.search_file)
    
@dp.message_handler(state=StateSearch.search_file)
async def main_search_result(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer("Kitob nomini matn ko'rinishida kiriting:")
        return
    await state.update_data(search_file=message.text)
    
    data = await state.get_data()
    search_file_ = data.get("search_file")
    await state.finish()
    await state.reset_state()

    products = await search_result(search_file_)
    await message.answer("Qidiruv bo'yicha mos kelgan kitoblar:", reply_markup=products)    

#--------------   Category add   --------------------

@dp.message_handler(text="Kategoriya qo'shish", user_id=ADMIN, state="*")
async def add_book(message: types.Message, state: FSMContext):
    await message.answer("Kategoriya nomini yuboring: ")
    await state.set_state(StateData.category_name)

#--------------   Book add   --------------------

@dp.message_handler(text="Kitob qo'shish", user_id=ADMIN, state="*")
async def add_book(message: types.Message, state: FSMContext):
    await message.answer("Kitob nomini yuboring: ")
    await state.set_state(StateData.file_name)

@dp.message_handler(state=StateData.file_name)
async def echo(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer("Kitob nomini matn ko'rinishida kiriting:")
        return
    await state.update_data(file_name=message.text)
    await message.answer("Kitob kategoriya idsini kiriting:")
    await StateData.next()

@dp.message_handler(state=StateData.category_id)
async def echo(message: types.Message, state: FSMContext):
    print(message.text)
    if message.text.isalpha():
        await message.answer("Kitob kategoriya idsini raqam ko'rinishida kiriting:")
        return
    await state.update_data(category_id=message.text)
    await message.answer("Kitob haqida ma'lumotni kiriting:")
    await StateData.next()

@dp.message_handler(state=StateData.file_des)
async def echo(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer("Kitob ma'lumotini matn ko'rinishida kiriting!")
        return
    await state.update_data(file_des=message.text)
    await message.answer("Kitob narxini kiriting:")
    await StateData.next()

@dp.message_handler(state=StateData.file_price)
async def echo(message: types.Message, state: FSMContext):
    if message.text.isalpha():
        await message.answer("Kitob narxini to'g'ri ko'rinishda kiriting: misol (10000)")
        return
    await state.update_data(file_price=message.text)
    await message.answer("Kitob rasmini yuboring:")
    await StateData.next()

@dp.message_handler(content_types="any", state=StateData.file_photo)
async def echo(message: types.Message, state: FSMContext):
    if message.content_type != "photo":
        await message.answer("Kitob rasmini png yoki jpeg formatda yuboring:")
        return
    await state.update_data(file_photo=message.photo[-1]["file_id"])
    await message.answer("Kitob faylini yuboring:")
    await StateData.next()

@dp.message_handler(content_types="any", state=StateData.file_text)
async def echo(message: types.Message, state: FSMContext):
    if message.content_type != "document":
        await message.answer("Kitob pdf faylini yuboring:")
        return

    await state.update_data(file_text=message.document["file_id"])
    
    data = await state.get_data()
    file_name_ = data.get("file_name").capitalize()
    category_id_ = data.get("category_id")
    file_des_ = data.get("file_des")
    file_price_ = data.get("file_price")
    file_photo_ = data.get("file_photo")
    file_text_ = data.get("file_text")

    db.insert_products(file_name_, file_des_, category_id_, file_price_, file_photo_, file_text_)

    await state.finish()
    await state.reset_state()
    await message.answer("Ma'lumotlaringiz saqlandi!")
    await message.answer_photo(photo=file_photo_, caption=f"{file_name_}\n{file_des_}")
    await message.answer_document(document=file_text_)

#--------------   Number of users   --------------------

@dp.message_handler(commands=['users'], user_id=ADMIN)
async def count(message: types.Message):
    data = db.count_users()
    await message.answer(f"Foydalanuvchilar soni: {data[0]} ta")

#--------------   Others   --------------------

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

#--------------   Bot end   --------------------
