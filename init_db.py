import sqlite3
import user_db

def construct_db(admin_id, admin_password):
	"""
	Initializes and creates a database
	"""
	connection = sqlite3.connect('users.db')
	cursor = connection.cursor()
	try:
		cursor.execute("CREATE TABLE users (user_id UNIQUE, hashed_password, salt, access_level)")
	except:
		print("\nDATABASE already exists. If you want to re-initialize the database, please delete users.db and run init_db.py\n")
		return

	salt = user_db.salt_generator()
	hashed_password = user_db.hash_function(admin_password + salt)

	cursor.execute("INSERT INTO users VALUES (?,?,?,?)", (admin_id, hashed_password, salt, 'administrator'))
	cursor.execute("SELECT * FROM users")
	print('--------------------------------------------')
	print('\nAdministrator account setup is complete. ')
	print('You are ready to run user_db.py\n')
	print('--------------------------------------------')
	print(cursor.fetchall())
	connection.commit()
	connection.close()

if __name__ == "__main__":
	construct_db(input('\nType a desired admin_id: '), input('Type a desired admin_password: '))
