import config, login

#login and connect to db
user_id = login.login()
conn = config.connection
cur = conn.cursor()

# get user input
print("1. Projected Budget")
print("2. Actual Transactions")
option = input("Select an option: ")

# query and return data
while True:
    if option == "1":
        cur.execute("""SELECT SUM(b.amount) from budget_items b
        JOIN categories c ON c.id = b.category_id
        WHERE c.id <> 7 AND
        user_id = %s""", (user_id,))
        total_expense = cur.fetchall()
        expense = total_expense[0][0]
        cur.execute("""SELECT SUM(b.amount) from budget_items b
        JOIN categories c ON c.id = b.category_id
        WHERE c.id = 7 AND
        user_id = %s""", (user_id,))
        total_income = cur.fetchall()
        income = total_income[0][0]
        net = income - expense
        formatted_net = "${:,.2f}".format(abs(net))
        if net < 0:
            print(f"The budget created suggests spending {formatted_net} more than income.")
            break
        elif net > 0:
            print(f"The budget created suggests earning {formatted_net} more than expenses.")
            break
        else: 
            print("The budget created suggests spending equal to earnings.")
            break
    elif option == "2":
        cur.execute("""SELECT SUM(t.amount) from transactions t
        JOIN categories c ON c.id = t.category_id
        WHERE c.id <> 7 AND
        user_id = %s""", (user_id,))
        total_expense = cur.fetchall()
        if total_expense[0][0] is None:
            expense = 0 
        else:
            expense = total_expense[0][0]
        cur.execute("""SELECT SUM(t.amount) from transactions t
        JOIN categories c ON c.id = t.category_id
        WHERE c.id = 7 AND
        user_id = %s""", (user_id,))
        total_income = cur.fetchall()
        if total_income[0][0] is None:
            income = 0
        else:
            income = total_income[0][0]
        net = income - expense
        formatted_net = "${:,.2f}".format(abs(net))
        if net < 0:
            print(f"Spending is {formatted_net} greater than income.")
            break
        elif net > 0:
            print(f"Earnings are {formatted_net} greater than expenses.")
            break
        else: 
            print("Earnings is equal to spending.")
            break
    else:
        print("Select '1' or '2'")
