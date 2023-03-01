import psycopg2

API_KEY ="ca7286427f2a13ee7461c1bd799b3a45"
ALPHA_KEY = "V3VL5V9O18Y57H8X" #ALPHA VANTAGE
NEWS_API_KEY = "bf1039159e414b7b865341206cd8e984" # News API

connection = psycopg2.connect(
    dbname="investment_dashboard",
    user="postgres",
    password="7TQs5%a!SNxvM1By!4El",
    host="localhost",
    port="5434"
)

