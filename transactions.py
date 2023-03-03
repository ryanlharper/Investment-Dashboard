import config, datetime
import math
import hashlib, secrets

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

conn = config.connection
cur = conn.cursor()
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
            break
        else:
            print("Username and password do not match.")
            continue

    # user input transaction data
    while True:
        type = input("Enter transaction type (buy, sell or q to quit): ").lower()
        if type == "buy" or type == "b":
            action = "in"
            symbol = input('Enter symbol: ').upper() #Cannot be NULL
            cost = float(input('Enter cost per share: '))# Cannot be NULL
            while True:
                buy_date = input('Enter purchase date (YYYY-MM-DD): ') # Can be NULL
                try:
                    # Parse the input string into a datetime object
                    date_obj = datetime.datetime.strptime(buy_date, "%Y-%m-%d")
                    # Format the datetime object as a string in the proper SQL DATE format
                    buy_date_str = date_obj.strftime("%Y-%m-%d")
                    break
                except ValueError:
                    # Handle the case where the user entered an invalid date string
                    print("Invalid format. Please enter in YYYY-MM-DD format.")
                    continue
            while True:
                number_shares_str = input('Enter number of shares: ') # Can be NULL
                try:
                    number_shares = float(number_shares_str)
                    int_shares = math.floor(number_shares) 
                    if number_shares >= 0:
                            break
                    else: 
                        print("Please enter a number grater than zero.")
                except ValueError: 
                    print("Invalid input. Please enter a valid number.")
                    continue
            break
        elif type == "sell" or type =="s":
            action = "out"
            while True:
                symbol = input("Enter symbol: ").upper() # Cannot be NULL
                cur.execute("SELECT symbol FROM positions")
                result_set = cur.fetchall()
                if symbol in [row[0] for row in result_set]:
                    break
                else:
                    print("Symbol does not exist in positions table.")
                    continue
            price = float(input("Enter the sell price: ")) # Cannot be NULL
            while True:
                sell_date = input('Enter sell date (YYYY-MM-DD): ') # Can be NULL
                try:
                    # Parse the input string into a datetime object
                    date_obj = datetime.datetime.strptime(sell_date, "%Y-%m-%d")
                    # Format the datetime object as a string in the proper SQL DATE format
                    sell_date_str = date_obj.strftime("%Y-%m-%d")
                    break
                except ValueError:
                    # Handle the case where the user entered an invalid date string
                    print("Invalid format. Please enter in YYYY-MM-DD format.")
                    continue
            # Retrieve the current number of shares for the symbol input from the positions table
            cur.execute("SELECT number_shares FROM positions WHERE symbol = ?", (symbol,))
            current_shares = cur.fetchone()[0]
            while True:
                number_shares_str = input('Enter number of shares: ') # Can be NULL
                try:
                    number_shares = float(number_shares_str)
                    int_shares = math.floor(number_shares) 
                    if number_shares >= 0 and number_shares <= current_shares:
                        break
                    elif number_shares < 0:
                        print("Please enter a number greater than or equal to zero.")
                    else:
                        print("You cannot sell more shares than you currently own.")
                except ValueError: 
                    print("Invalid input. Please enter a valid number.")
                    continue
            break
        elif type == "q":
            exit()
        else:
            print("\nOnly buys and sell transactions are permitted. ")
            print("Please enter buy or sell, or press q to quit.")
            continue



    # adjust the position in the database 
    if action == "in":
        buy_amount = number_shares * cost
        cur.execute("INSERT INTO positions (symbol, cost, buy_date, number_shares, user_id) VALUES (%s, %s, %s, %s, %s)", (symbol, cost, buy_date_str, number_shares, user_id))
        conn.commit()

        # insert transaction data into transactions table
        cur.execute("INSERT INTO transactions (type, symbol, buy_price, amount, date, user_id, number_shares) VALUES (%s, %s, %s, %s, %s, %s, %s)", ("buy", symbol, cost, buy_amount, buy_date_str, user_id, number_shares))
        conn.commit()

    elif action == "out":
        sell_amount = number_shares * price
        if current_shares == number_shares:
            cur.execute("DELETE FROM positions WHERE symbol = %s", (symbol))
            conn.commit()

            # insert transaction data into transactions table
            cur.execute("INSERT INTO transactions (type, symbol, sell_price, amount, date, user_id, number_shares) VALUES (%s, %s, %s, %s, %s, %s, %s)", ("sell", symbol, price, sell_amount, sell_date_str, user_id, number_shares))
            conn.commit()

        else:
            new_shares = current_shares - number_shares
            cur.execute("UPDATE positions SET number_shares = %s WHERE symbol = %s", (new_shares))
            conn.commit()

            # insert transaction data into transactions table
            cur.execute("INSERT INTO transactions (type, symbol, sell_price, amount, date, user_id, number_shares) VALUES (%s, %s, %s, %s, %s, %s, %s)", ("sell", symbol, price, sell_amount, sell_date_str, user_id, number_shares))
            conn.commit()

    else:
        print("There was an error processing the transaction. Please try again.")
        exit()
    break
# close connection
cur.close()
conn.close()