import config, datetime, login
import math

user_id = login.login()

conn = config.connection
cur = conn.cursor()
while True:
    # user input transaction data
    while True:
        type = input("Enter transaction type (buy, sell, income, expense or q to quit): ").lower()
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
        elif type == "income" or type == "expense":
                action = "budget"
                cur.execute("SELECT MAX(id) FROM transactions")
                max_transaction_id = cur.fetchone()[0]
                new_transaction_id = max_transaction_id + 1 
                while True:
                    try:
                        budget_amount = round(float(input("Enter transaction amount: ")), 2)
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                while True:
                    trans_date = input('Enter transaction date (YYYY-MM-DD): ') 
                    try:
                        # Parse the input string into a datetime object
                        date_obj = datetime.datetime.strptime(trans_date, "%Y-%m-%d")
                        # Format the datetime object as a string in the proper SQL DATE format
                        trans_date_str = date_obj.strftime("%Y-%m-%d")
                        break
                    except ValueError:
                        # Handle the case where the user entered an invalid date string
                        print("Invalid format. Please enter in YYYY-MM-DD format.")
                        continue
                description = input("Enter transaction description: ")
                cur.execute("SELECT c.id, c.name FROM categories c")
                all_categories = cur.fetchall()
                numeral = 0
                for category in all_categories:
                    numeral += 1
                    print(f"{numeral}. {category[1]}")
                while True:
                    try:
                        category_id = int(input("Please choose a category: ")) - 1
                        if 0 <= category_id < len(all_categories):
                            break
                        else:
                            print("Invalid category ID. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                chosen_category = all_categories[category_id]
                category_id = chosen_category[0]
                cur.execute("SELECT sc.id, sc.name FROM subcategories sc")
                all_subcategories = cur.fetchall()
                numeral = 0
                for subcategory in all_subcategories:
                    numeral += 1
                    print(f"{numeral}. {subcategory[1]}")
                while True:
                    try:
                        subcategory_id = int(input("Please choose a subcategory: ")) - 1
                        if 0 <= subcategory_id < len(all_subcategories):
                            break
                        else:
                            print("Invalid subcategory ID. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                chosen_subcategory = all_subcategories[subcategory_id]
                subcategory_id = chosen_subcategory[0]
        elif type == "q":
            exit()
        else:
            print("\nOnly buy, sell, income and expense transactions are permitted. ")
            print("Please enter buy or sell, or press q to quit.")
            continue

    # adjust the position in the database 
    if action == "in":
        buy_amount = number_shares * cost
        cur.execute("INSERT INTO positions (symbol, cost, buy_date, number_shares, user_id) VALUES (%s, %s, %s, %s, %s)", (symbol, cost, buy_date_str, number_shares, user_id))
        conn.commit()

        # insert transaction data into transactions table
        cur.execute("INSERT INTO transactions (type, symbol, buy_price, amount, date, user_id, number_shares, category_id, subcategory_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", ("buy security", symbol, cost, buy_amount, buy_date_str, user_id, number_shares, 10, 31))
        conn.commit()

    elif action == "out":
        sell_amount = number_shares * price
        if current_shares == number_shares:
            cur.execute("DELETE FROM positions WHERE symbol = %s", (symbol))
            conn.commit()

            # insert transaction data into transactions table
            cur.execute("INSERT INTO transactions (type, symbol, sell_price, amount, date, user_id, number_shares, category_id, subcategory_id) VALUES (%s, %s, %s, %s, %s, %s, %s, 10 ,33)", ("sell security", symbol, price, sell_amount, sell_date_str, user_id, number_shares, 7, 25))
            conn.commit()

        else:
            new_shares = current_shares - number_shares
            cur.execute("UPDATE positions SET number_shares = %s WHERE symbol = %s", (new_shares))
            conn.commit()

            # insert transaction data into transactions table
            cur.execute("INSERT INTO transactions (type, symbol, sell_price, amount, date, user_id, number_shares, category_id, subcategory_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", ("sell security", symbol, price, sell_amount, sell_date_str, user_id, number_shares, 7, 25))
            conn.commit()

    elif action == "budget":
        if category_id == 7:
            # insert income transaction data into transactions table
            cur.execute("INSERT INTO transactions (id, type, amount, date, user_id, description, category_id, subcategory_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", (new_transaction_id, "income", budget_amount, trans_date_str, user_id, description, category_id, subcategory_id))
            conn.commit()
        else: 
            # insert income transaction data into transactions table
            cur.execute("INSERT INTO transactions (id, type, amount, date, user_id, description, category_id, subcategory_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", (new_transaction_id, "expense", budget_amount, trans_date_str, user_id, description, category_id, subcategory_id))
            conn.commit() 
    else:
        print("There was an error processing the transaction. Please try again.")
        exit()
    break
# close connection
cur.close()
conn.close()