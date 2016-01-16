'''
Python3 simple login script
December 10, 2015
Written by Tony Lee

'''
import os, sys, sqlite3, string, random, hashlib

DATABASE = 'users.db'
connection = None
admin_access = False

'''
Database methods
1) get_db()
2) get_all_users()
3) add_user(user_id, password)
4) check_user(user_id)
5) authenticate_credentials(user_id, password)
6) salt_generator()
7) hash_function(password_salt)
'''
def get_db():
    try:
        global connection
        if connection:
            return connection
        connection = sqlite3.connect(DATABASE)
        return connection
    except:
        print('\nUnexpected error: contact your administrator.\n')

def get_all_users_db():
    cursor = get_db().cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE access_level = 'user'")
        return cursor.fetchall()
    except:
        print('\nUnexpected error: contact your administrator.\n')
        return

def add_user_db(user_id, password):
    try:
        get_db().cursor().execute("INSERT INTO users VALUES (?,?,?)", (user_id, password, 'user'))
        get_db().commit()
    except:
        print('\nFailed: User already exists in the database.\n')

def get_user_db(user_id):
    cursor = get_db().cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE access_level = 'user' AND user_id = ?", (user_id,))
        data = cursor.fetchall()
        if data == []:
            print("\nUser doesn't exist in the database.\n")
            return False
        print('\nUser_id: ' + str(data[0][0]))
        print('Hashed_password: ' + str(data[0][1]))
        print('Salt: ' + str(data[0][1]))
        print('Access_level: ' + str(data[0][3]) + '\n')
        return True
    except:
        print('\nUnexpected error: contact your administrator.\n')
        return False

def authenticate_credentials_db(user_id, password):
    cursor = get_db().cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        data = cursor.fetchall()
        if data[0][0] == user_id:
            if hash_function(password + data[0][2]) == data[0][1]:
                print("\nCredential authentication successful.\n")
                if data[0][3] == 'administrator':
                    global admin_access
                    admin_access = True
                return True
            else:
                print("\nIncorrect password.\n")
                return False
        else:
            print("\nIncorrect user_id.\n")
            return False
    except:
        print('\nCredential authentication failed.\n')
        return False

def salt_generator():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(512))

def hash_function(password_salt):
    hashed_val = 0
    for c in password_salt:
        hashed_val += 534 ^ ord(c) * 193092
    return hashed_val 

'''
System methods
1) ask_credentials()
2) main()
3) admin_mode()
'''
def ask_credentials():
    return [input('Enter a user id: '), input('Enter a password: ')]

def main():
    print('\n################################################')
    print('############# User Database System #############')
    print('################################################\n')

    user_id, password = ask_credentials()
    if not authenticate_credentials_db(user_id, password):
        print('Login credentials are invalid.\n')
        return
    else:
        # general user
        if not admin_access:
            print('Non admin user is not currently supported.\n')
            return
        # admin case
        else:
            print('Login successful as an administrator.\n')
            admin_mode()
            return

def admin_mode():
    line_count = 1
    print('Type "help" to see the list of commands')
    while True:
        command = input('[' + str(line_count) + ']' + ' >>> ')
        if command == 'add_user':
            add_user(input('Enter a user id: '), input('Enter a password: '))
        elif command == 'get_user':
            get_user(input('Enter a user id: '))
        elif command == 'display_users':
            display_users()
        elif command == 'log_out':
            print('\nSuccessfuly logged out.\n')
            break
        elif command == 'help':
            help()
        line_count += 1
    return

'''
Admin methods
1) add_user(user_id, password)
2) get_user(user_id)
3) display_users()
4) help()
'''
def add_user(user_id, password):
    add_user_db(user_id, password)

def get_user(user_id):
    get_user_db(user_id)

def display_users():
    users = get_all_users_db()
    if users == []:
        print('\n    No users yet.\n')
        return
    print('')
    for user in users:
        print(user)
    print('')

def help():
    print('\nType commands: \n')
    print('add_user')
    print('display_users')
    print('log_out')
    print('')

if __name__ == "__main__":
    main()