import config, datetime, login
import math

user_id = login.login()  

conn = config.connection
cur = conn.cursor()

transactions = [] # for entry to transactions
positions= [] # for entry to positions (buy and partial sell)  !!! NEED TWO (one for buy - one for p seel... need four total lists)
positions_full_sell = []

while True:
    # user input transaction data
    while True:
        type = input("Enter transaction type (buy, sell or q to quit): ").lower()
        if type == "buy":
            while True:
                symbol = input('Enter symbol: ').upper() #Cannot be NULL
                if symbol == "":
                    print("Symbol must be entered.")
                    continue
                else:
                    break
            while True:   # add error handling for non-numeric input
                cost = float(input('Enter cost per share: '))# Cannot be NULL
                if cost == "" or cost < 0:
                    print("Cost per share must be a positive number.")
                    continue
                else:
                    break
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
                number_shares_str = input('Enter number of shares: ') # Can be NULL but invalid transaction with code here
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
            transactions.append((type, symbol, cost, buy_date_str, user_id, number_shares))
            positions.append((symbol, cost, buy_date_str, number_shares, user_id))
            break
        elif type == "sell":
            while True:
                symbol = input("Enter symbol: ").upper() # Cannot be NULL
                if symbol =="":
                    print("Symbol must be entered.")
                    continue
                cur.execute("SELECT symbol FROM positions")
                result_set = cur.fetchall()
                if symbol in [row[0] for row in result_set]:
                    break
                else:
                    print("Symbol does not exist in positions table.")
                    continue
            while True:   # add error handling for non-numeric input
                price = float(input("Enter the sell price: ")) # Cannot be NULL
                if price == "" or price < 0:
                    print("Price must be a positive number.")
                    continue
                else:
                    break
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
            cur.execute("SELECT number_shares FROM positions WHERE symbol = %s AND user_id = %s", (symbol, user_id))
            current_shares = cur.fetchone()[0]
            while True:
                number_shares_str = input('Enter number of shares: ') # Can be NULL but stopping invalid transaction with code here
                try:
                    number_shares = float(number_shares_str)
                    int_shares = math.floor(number_shares) 
                    if number_shares >= 0 and number_shares < current_shares: #partial sell
                        positions.append((current_shares - int_shares, user_id))
                        break
                    elif number_shares == current_shares:
                        positions_full_sell.append((symbol, user_id))
                        break
                    elif number_shares < 0:
                        print("Please enter a number greater than zero.")
                    else:
                        print("You cannot sell more shares than you currently own.")
                except ValueError: 
                    print("Invalid input. Please enter a valid number.")
                    continue
            transactions.append(type, symbol, price, sell_date_str, user_id, number_shares)
            break
        elif type == "q":
            break
        else:
            print("\nOnly buy or sell transactions are permitted. ")
            print("Please enter 'buy', 'sell' or press q to quit.")
            continue

    # adjust the position in the database 
    if type == "buy":
        cur.execute("INSERT INTO positions (symbol, cost, buy_date, number_shares, user_id) VALUES (%s, %s, %s, %s, %s)", (positions,))
        conn.commit()

        # insert transaction data into transactions table
        cur.execute("INSERT INTO transactions (type, symbol, buy_price, date, user_id, number_shares) VALUES (%s, %s, %s, %s, %s, %s)", (transactions,))
        conn.commit()

    elif type == "sell":
        if current_shares == number_shares:
            cur.execute("DELETE FROM positions WHERE symbol = %s AND user_id = %s", (positions_full_sell,))
            conn.commit()

            # insert transaction data into transactions table
            cur.executemany("INSERT INTO transactions (type, symbol, sell_price, date, user_id, number_shares) VALUES (%s, %s, %s, %s, %s, %s)", (transactions,))
            conn.commit()

        else:
            cur.execute("UPDATE positions SET number_shares = %s WHERE symbol = %s AND user_id = %s", (positions,))
            conn.commit()

            # insert transaction data into transactions table
            cur.executemany("INSERT INTO transactions (type, symbol, sell_price, date, user_id, number_shares) VALUES (%s, %s, %s, %s, %s, %s)", (transactions,))
            conn.commit()

    # close connection
    cur.close()
    conn.close()