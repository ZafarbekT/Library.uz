from aiogram.dispatcher.filters.state import State, StatesGroup

class StateData(StatesGroup):
	file_name = State()
	category_id = State()
	file_des = State()
	file_price = State()
	file_photo = State()
	file_text = State()

class StateSearch(StatesGroup):
	search_file = State()

class StateCategory(StatesGroup):
	category_name = State()