import psycopg2
import win32com.client as win32

# Set email parameters
recipient = "ryan@vcm.us.com"
subject = "Next Week's Earnings Reports"
message = "Here are companies reporting earnings next week:"

# Connect to database and execute query
conn = psycopg2.connect(
    dbname="vcm_holdings",
    user="postgres",
    password="",
    host="localhost",
    port="5432"
)

cur = conn.cursor()
query = """
SELECT symbol AS "Symbol", earnings_date AS "Earnings Date", to_char(earnings_date, 'Dy') AS "Day of Week"
FROM earnings_dates
WHERE earnings_date BETWEEN CURRENT_DATE AND CURRENT_DATE + 7
ORDER BY earnings_date;
"""
cur.execute(query)
results = cur.fetchall()
conn.close()

# Format results as a string
results_str = ""
for row in results:
    results_str += f"{row[0]} - {row[1]} ({row[2]:>3})\n"

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = recipient   
mail.Subject = subject
mail.Body = message + "\n\n" + results_str

# Send email
mail.Send()
