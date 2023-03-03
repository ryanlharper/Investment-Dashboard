import config, datetime
import login

user_id = login.login()
    
# user set goal
while True: 
    goal = input("Describe the goal or press q to quit: ")
    if goal == "q":
        exit()
    elif goal == "":
        print("Please describe the goal as a reminder: ")
        continue
    else:
        break
while True:
    type = input("Enter type of goal (amount or percent) or press q to quit: ").lower()
    if type == "q":
        exit()
    elif type == "amount" or type =="percent":
        break
    else:
        print("Please enter 'amount' or 'percent'.")
        continue
while True:
    deadline_str = input("Enter the deadline for this goal (YYYY-MM-DD) or enter q to quit: ")
    if deadline_str == "q":
        exit()
    else:    
        try:
            # Parse the input string into a datetime object
            deadline = datetime.datetime.strptime(deadline_str, "%Y-%m-%d").date()
            break
        except ValueError:
            # Handle the case where the user entered an invalid date string
            print("Invalid format. Please enter in YYYY-MM-DD format.")
            continue
while True: 
    begin_value = round(float(input("Enter the begining value or enter q to quit: ")),2)
    if begin_value =="q":
        exit()
    else: 
        break
while True:
    if type == "amount":
        while True:
            try:
                goal_value = round(float(input("Enter the value of the goal: ")),2)
                if goal_value <= 0:
                    print("Invalid input. Please enter a number greater than zero.")
                else:
                    break
            except (ValueError, ZeroDivisionError):
                print("Invalid input. Please enter a numerical value.")
    else:
        while True:
            try:
                goal_percent = round(float(input("Enter the annualized return goal: ")),2)
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value.")
        break
    break

conn = config.connection
cur = conn.cursor()
# get current value from portfolios
cur.execute("SELECT SUM(market_value) from positions WHERE user_id = %s", (user_id,))
current_value = cur.fetchone()[0]

# set goal dates
today = datetime.date.today()
time_diff = deadline - today
seconds_to_goal = time_diff.total_seconds()
years_to_goal = seconds_to_goal / (365.2425 * 24 * 60 * 60)
days_to_goal = time_diff.days

# insert into sql table and print summary
if type == "amount":   
    cur.execute("INSERT INTO goals (goal, type, deadline, begin_value, goal_value, current_value, date, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (goal, type, deadline_str, begin_value, goal_value, current_value, today, user_id))
    conn.commit()
    goal_return = ((float(goal_value) - float(current_value)) / float(current_value))
    annualized_goal_return = (goal_return / years_to_goal)
    print("To reach this goal by", deadline, "the portfolio will need to return", str(round(goal_return,2)*100)+"%, which is an annualized return of", str(round(annualized_goal_return,2)*100) +"%." )
elif type == "percent":
    cur.execute("INSERT INTO goals (goal, type, deadline, begin_value, goal_percent, current_value, date, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (goal, type, deadline_str, begin_value, goal_percent, current_value, today, user_id))
    conn.commit()
    end_goal_amount = ((days_to_goal*(goal_percent/365))*current_value)+current_value
    print("If the goal is met, by", deadline, "the portfolio will be valued at $" + str(end_goal_amount)+".")


cur.close()
conn.close()
    

