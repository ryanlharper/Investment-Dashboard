import hashlib, secrets, config

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest(), salt

conn = config.connection
cur = conn.cursor()

# User data
first_name = input('Enter your first name: ') #Can be NULL
last_name = input('Enter your last name: ') # Can be NULL
username = input('Enter your username: ') # Cannot be NULL
email = input('Enter your email: ') # Cannot be NULL
password = input('Enter your password: ') # Cannot be NULL

# Hash and salt the password
hashed_password, salt = scramble(password)

# Insert the user into the database with the hashed and salted password
cur.execute("INSERT INTO users (first_name, last_name, username, email, password, salt) VALUES (%s, %s, %s, %s, %s, %s)", (first_name, last_name, username, email, hashed_password, salt))
conn.commit()

cur.close()
conn.close()
