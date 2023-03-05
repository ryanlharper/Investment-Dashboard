import config, login
import matplotlib.pyplot as plt

user_id = login.login()

conn = config.connection
cur = conn.cursor()
cur.execute("""SELECT sc.name, ROUND(b.amount,0) FROM budget_items b 
JOIN subcategories sc on sc.id = b.subcategory_id 
JOIN categories c ON c.id = sc.category_id
WHERE b. amount > 0 
AND c.id <> 7
AND b.user_id = %s""", (user_id,))
budget_list = cur.fetchall()

categories = [item[0] for item in budget_list]
amounts = [item[1] for item in budget_list]

plt.pie(amounts, labels=categories)

plt.show()

