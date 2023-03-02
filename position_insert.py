import config
conn = config.connection
cur = conn.cursor()

# User data - need to add error handling
type = input("Is this a buy transaction? ").lower()
if type == "yes" or type == "y":
    symbol = input('Enter symbol: ').upper() #Cannot be NULL
    cost = float(input('Enter cost: '))# Cannot be NULL
    buy_date = input('Enter purchase date: ') # Can be NULL
    number_shares = input('Enter number of shares: ') # Can be NULL
else:
    print("Sell transactions coming soon.")

# Insert the position into the database 
cur.execute("INSERT INTO positions (symbol, cost, buy_date, number_shares) VALUES (%s, %s, %s, %s)", (symbol, cost, buy_date, number_shares))
conn.commit()

cur.close()
conn.close()