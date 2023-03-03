import config, login
import re, email.utils

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
    else:
        cur.execute("SELECT username FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        if result is not None:
            print("username", username, "already registered.")
            continue
        else:
            break
# enter and check email
while True:
    email_str = input('Enter your email or enter q to quit: ')
    if email_str == "q":
        exit()    
    elif email_str == "":
        print("An email address must be entered to register.")
        continue
    else:
        try:
            parsed_email = email.utils.parseaddr(email_str)
            if not re.match(r"[^@]+@[^@]+\.[^@]+", parsed_email[1]):
                raise ValueError
            cur.execute("SELECT email FROM users")
            email_list = cur.fetchall()
            if parsed_email[1] in [row[0] for row in email_list]:
                print("Email address", parsed_email[1], "is already registered.")
                continue
            else:
                break
        except ValueError:
            print("Please enter a valid email address.")
            continue
# enter and check password
while True:
    password = input('Enter your password or enter q to quit: ') # Cannot be NULL
    if password == "q":
        exit()
    elif len(password) <=7:
        print("Password must be eight characters or greater.")
        continue
    else:
        break

# Hash and salt the password
hashed_password, salt = login.scramble(password)

# Insert the user into the database with the hashed and salted password
cur.execute("INSERT INTO users (first_name, last_name, username, email, password, salt) VALUES (%s, %s, %s, %s, %s, %s)", (first_name, last_name, username, email_str, hashed_password, salt))
conn.commit()

cur.close()
conn.close()
