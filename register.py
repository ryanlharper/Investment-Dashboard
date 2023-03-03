import hashlib, secrets, config

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest(), salt

conn = config.connection
cur = conn.cursor()

# registration input data
first_name = input('Enter your first name: ') #Can be NULL
last_name = input('Enter your last name: ') # Can be NULL

# enter and check username 
while True:
    username = input('Enter your username or enter q to quit: ') # Cannot be NULL
    if username == "q":
        exit()
    elif len(username) <=6:
        print("username must be greater than six characters.")
        continue
    elif len(username) > 6:
        cur.execute("SELECT username FROM users")
        users_list = cur.fetchall()
        if username in [row[0] for row in users_list]:
            print("username", username, "already registered.")
            continue
    else:
        break
# enter and check email
while True:
    email = input('Enter your email or enter q to quit: ') # Cannot be NULL
    if email == "q":
        exit()    
    elif email == "":
        print("An email address must be entered to register.")
        continue
    elif email != "":
        cur.execute("SELECT email FROM users")
        email_list = cur.fetchall()
        if email in [row[0] for row in email_list]:
            print("Email adress", email, "is already registered.")
            continue
    elif "@" not in email:
        print("Please enter a valid email address.") 
        continue
    else:
        break
# enter and check password
while True:
    password = input('Enter your password or enter q to quit: ') # Cannot be NULL
    if password == "q":
        exit()
    elif password <=7:
        print("Password must be eight characters or greater.")
        continue
    else:
        break

# Hash and salt the password
hashed_password, salt = scramble(password)

# Insert the user into the database with the hashed and salted password
cur.execute("INSERT INTO users (first_name, last_name, username, email, password, salt) VALUES (%s, %s, %s, %s, %s, %s)", (first_name, last_name, username, email, hashed_password, salt))
conn.commit()

cur.close()
conn.close()
