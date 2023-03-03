import config, datetime, login
import math

user_id = login.login()

conn = config.connection
cur = conn.cursor()
while True:
    # user input transaction data
    while True:
        type = input("Enter transaction type (buy, sell or q to quit): ").lower()
        if type == "buy" or type == "b":
            action = "in"
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
            break
        elif type == "sell" or type =="s":
            action = "out"
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
            cur.execute("SELECT number_shares FROM positions WHERE symbol = ?", (symbol,))
            current_shares = cur.fetchone()[0]
            while True:
                number_shares_str = input('Enter number of shares: ') # Can be NULL but stopping invalid transaction with code here
                try:
                    number_shares = float(number_shares_str)
                    int_shares = math.floor(number_shares) 
                    if number_shares >= 0 and number_shares <= current_shares:
                        break
                    elif number_shares < 0:
                        print("Please enter a number greater than zero.")
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