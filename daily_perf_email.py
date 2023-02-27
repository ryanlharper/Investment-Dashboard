import config
import win32com.client as win32

# Set email parameters
recipient = "ryan@vcm.us.com"
subject = "Daily Performance"
message = ""

# Connect to database and execute queries
conn = config.connection

cur = conn.cursor()
query1 = """
SELECT symbol, ROUND(change_pct,2) 
FROM watchlist 
ORDER BY change_pct DESC LIMIT 5;
"""

query2 = """
SELECT symbol, ROUND(change_pct,2) 
FROM watchlist 
ORDER BY change_pct ASC LIMIT 5;
"""

cur.execute(query1)
top_results = cur.fetchall()

cur.execute(query2)
bottom_results = cur.fetchall()

conn.close()

# Format results as a string
results_str = ""
for row in top_results:
    results_str += f"{row[0]}: {row[1]}%\n"

message += "Top Performers:\n\n" + results_str + "\n"

results_str = ""
for row in bottom_results:
    results_str += f"{row[0]}: {row[1]}%\n"

message += "Bottom Performers:\n\n" + results_str

# Create Outlook application and mail item
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = recipient
mail.Subject = subject
mail.Body = message

# Send email
mail.Send()
