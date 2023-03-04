import config
import login

# get user_id from login function
user_id = login.login()

# establish db connection and prompt user for budget year
conn = config.connection
cur = conn.cursor()
cur.execute("SELECT id, year FROM budget_years")
years = cur.fetchall()
for year in years:
    print(f"{year[0]}. {year[1]}")
while True:
    try:
        selected_year_num = int(input("Enter the number of the budget year: "))
        selected_year_id = years[selected_year_num - 1][0]
        break
    except (ValueError, IndexError):
        print("Invalid input. Please enter a number corresponding to a budget year.")

# query db and collect subcategories
cur = conn.cursor()
cur.execute("""SELECT c.id, c.name, sc.id, sc.name 
               FROM categories c JOIN subcategories sc ON sc.category_id = c.id""")
all_subcategories = cur.fetchall()
budget_list = []

for subcategory in all_subcategories:
    while True:
        try:
            amount = float(input(f"{subcategory[0]}.{subcategory[2]}. Enter annual budget amount for {subcategory[1]}: {subcategory[3]}> "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    budget_list.append((subcategory[0], subcategory[2], amount))

# check for additional budget items and insert is needed
while True:
    print("Do you have any budget items not included in these categories?")
    response = input("Enter (y or n): ").lower()
    if response == 'n':
        break
    elif response == 'y':
        category_name = input("Enter the category name: ")
        subcategory_name = input("Enter the subcategory name: ")
        amount = input("Enter the budget amount: ")
        cur.execute("SELECT MAX(id) FROM categories")
        max_category_id = cur.fetchone()[0]
        new_category_id = max_category_id + 1 
        cur.execute("SELECT MAX(id) FROM subcategories")
        max_subcategory_id = cur.fetchone()[0]
        new_subcategory_id = max_subcategory_id + 1 
        cur.execute("INSERT INTO categories (id, name) VALUES (%s, %s)", (new_category_id, category_name))
        conn.commit()
        cur.execute("""INSERT INTO subcategories (id, name, category_id) 
                       VALUES (%s, %s, %s)""",
                    (new_subcategory_id, subcategory_name, new_category_id))
        conn.commit()
        budget_list.append((new_category_id, new_subcategory_id, amount))

# insert budget items into budget_items table
for budget_item in budget_list:
    cur.execute("""INSERT INTO budget_items (amount, year_id, category_id, subcategory_id, user_id) 
                VALUES (%s, %s, %s, %s, %s)""",
                (budget_item[2], selected_year_id, budget_item[0], budget_item[1], user_id))
    conn.commit()

# insert to bridge table
for category_id, subcategory_id, amount in budget_list:
    if amount == '':
        continue 
    amount = float(amount)
    if amount != 0:
        cur.execute("""INSERT INTO user_category_subcategory_selections
                       (user_id, category_id, subcategory_id)
                       VALUES (%s, %s, %s)""",
                    (user_id, category_id, subcategory_id))
        conn.commit()

conn.close()
