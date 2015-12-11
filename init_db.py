import sqlite3

def construct_db(admin_id, admin_password):
	connection = sqlite3.connect('users.db')
	c = connection.cursor()
	try:
		c.execute("CREATE TABLE users (user_id UNIQUE, password, access_level)")
	except:
		print("\nDATABASE already exists. If you want to re-initialize the database, please delete users.db and run init_db.py\n")
		return
	c.execute("INSERT INTO users VALUES (?,?,?)", (admin_id, admin_password, 'administrator'))
	c.execute("SELECT * FROM users")
	print('\nAdmin setup is complete: ')
	print(str(c.fetchall()) + '\n')
	print('You are ready to run user_db.py\n')
	connection.commit()
	connection.close()

if __name__ == "__main__":
	construct_db(input('\nType a desired admin_id: '), input('Type a desired admin_password: '))
