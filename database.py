import sqlite3 

class Database():
	def __init__(self):
		self.conn = sqlite3.connect("books.db")
		self.cur = self.conn.cursor()

#---------------   Users   ----------------

	def create_users(self):
		self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
			tel_id VARCHAR(20),
			name VARCHAR(50)
			)""")

	def select_users(self, id):
		self.cur.execute(f"SELECT * FROM users WHERE tel_id = '{id}'")
		data = self.cur.fetchone()
		if data is None:
			return False
		else:
			return True

	def insert_users(self, tel_id, name):
		self.cur.execute(f"INSERT INTO users VALUES('{tel_id}', '{name}')")
		return self.conn.commit()

	def count_users(self):
		self.cur.execute(f"SELECT COUNT(*) FROM users")
		return self.cur.fetchone()

#---------------   Books Category   ----------------

	def create_category(self):
		self.cur.execute("""CREATE TABLE IF NOT EXISTS category(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name VARCHAR(20)
			)""")

	def insert_category(self, name):
		self.cur.execute(f"INSERT INTO category(name) VALUES('{name}')")
		return self.conn.commit()

	def select_category_id(self, id):
		self.cur.execute(f"SELECT * FROM category WHERE id = {id}")
		data = self.cur.fetchone()
		return data

	def select_category_all(self):
		self.cur.execute("SELECT * FROM category")
		data = self.cur.fetchall()
		return data 

#---------------   Books Products   ----------------

	def create_table_sub_products(self):
		self.cur.execute("""CREATE TABLE IF NOT EXISTS products(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			category_id INTEGER,
			file_text TEXT NULL,
			file_name VARCHAR(250),
			file_des TEXT NULL,
			file_photo TEXT NULL,
			file_price VARCHAR(20),
			FOREIGN KEY(category_id) references category(id)
			)""")

	def select_products_for_category_id(self, id):
		self.cur.execute(f"""SELECT * FROM products WHERE category_id = {id}""")
		return self.cur.fetchall()

	def select_product_id(self, id):
		self.cur.execute(f"""SELECT * FROM products WHERE id = {id}""")
		return self.cur.fetchone()

	def insert_products(self, file_name, file_des, category_id, file_price, file_photo, file_text):
		self.cur.execute(f"""INSERT INTO products(file_name, file_des, category_id, file_price, file_photo, file_text) values("{file_name}", "{file_des}", {category_id}, "{file_price}", "{file_photo}", "{file_text}")""" )
		return self.conn.commit()

	def search_book(self, search):
		self.cur.execute(f"""SELECT * FROM products WHERE file_name LIKE "%{search}%" """)
		return self.cur.fetchall()
