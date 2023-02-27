import config

def earnings():
    #Connect to database
    conn = config.connection

    #Query database
    cur = conn.cursor()
    query = """
    SELECT symbol AS "Symbol", earnings_date AS "Earnings Date", to_char(earnings_date, 'Day') AS "Day of Week"
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
    return results_str

results_str = earnings()
print(results_str)