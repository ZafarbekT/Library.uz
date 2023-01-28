from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from index import db

menu = ReplyKeyboardMarkup(
	keyboard = [
		[
			KeyboardButton(text="Kitoblar"),
			KeyboardButton(text="Qidirish")
		],
		[
			KeyboardButton(text="Aloqa")
		]
	], resize_keyboard = True
)

admin = ReplyKeyboardMarkup(
	keyboard = [
		[
			KeyboardButton(text="Kitob qo'shish"),
			KeyboardButton(text="Kategoriya qo'shish")
		],
		[
			KeyboardButton(text="Foydalanuvchilar soni")
		],
		[
			KeyboardButton(text="Orqaga qaytish")
		]
	], resize_keyboard = True
)

async def for_category_get_all():
	x = db.select_category_all()
	categories = InlineKeyboardMarkup(row_width = 2)
	for i in x:
		button_text = i[1]
		callback_data = i[0]
		categories.insert(
			InlineKeyboardButton(text=button_text, callback_data=f"productall_{callback_data}")
		)
	return categories

async def get_category_id(id):
	x = db.select_products_for_category_id(id)
	products = InlineKeyboardMarkup(row_width = 2)
	for i in x:
		button_text = i[3]
		callback_data = i[0]
		products.insert(
			InlineKeyboardButton(text=button_text, callback_data=f"products_{callback_data}")
		)
	return products

async def search_result(search):
	data = db.search_book(search)
	products = InlineKeyboardMarkup(row_width = 2)
	for i in data:
		button_text = i[3]
		callback_data = i[0]
		products.insert(
			InlineKeyboardButton(text=button_text, callback_data=f"products_{callback_data}")
		)
	return products