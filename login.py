import config
import hashlib, secrets

conn = config.connection
cur = conn.cursor()

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest(), salt

def check_password(username: str, password: str):
    """Check if the given username and password match a record in the SQL table"""
    cur.execute("SELECT id, username, password, salt FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user is None:
        return False
    hashed_password, salt = user[2], user[3]
    return hashed_password == hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

def login():
    #login & set user_id
    while True:
        while True:
            username = input("Enter username or press q to quit: ")
            if username == "q":
                exit()
            password = input("Enter password or press q to quit: ")
            if password == "q":
                exit()
            # check if the username and password match a record in the table
            if check_password(username, password):
                print("Login successful.")
                # set user_id equal to the id of the user with the matching username and password
                cur.execute("SELECT id FROM users WHERE username = %s", (username,))
                user_id = cur.fetchone()[0]
                return user_id
            else:
                print("Username and password do not match.")
                continue