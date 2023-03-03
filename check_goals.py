import config
import login, update_values, datetime

def progress_print():
    # print progress function
    print(f"Deadline: {deadline}")
    print(f"Begining value: ${begin_value}")
    print(f"Goal value: ${goal_value}")
    print(f"Current value: ${current_value}")
    print(f"Progress: {progress_percent:.2f}%")
    if years_to_goal < 1:
        print(f"Days to goal: {days_to_goal}")
    else:
        print(f"Years to goal: {years_to_goal:.2f}")
    print(f"Annualized return to date: {annualized_return:.2%}")
    print(f"Required return to meet goal: {required_return:.2%}")

# login & update portfolio values
user_id = login.login()
update_values.new_values()

# connect to db, query and return
conn = config.connection 
cur = conn.cursor()
cur.execute("SELECT goal, id, deadline, begin_value, goal_value, current_value, type, goal_percent FROM goals WHERE user_id = %s", (user_id,))
rows = cur.fetchall()
print("Goals:")
numeral = 0
for row in rows:
    numeral += 1
    print(str(numeral)+".", row[0])

#user select goal
goal_choice_index = int(input("Select a goal: ")) -1

# get goal data for selected goal
selected_goal = rows[goal_choice_index]
goal_id = selected_goal[1]
deadline = selected_goal[2]
begin_value = selected_goal[3]
goal_value = selected_goal[4]
current_value = selected_goal[5]
goal_type = selected_goal[6]
goal_percent = selected_goal[7]

# get goal date and set dates
today = datetime.date.today()
time_diff = deadline - today
seconds_to_goal = time_diff.total_seconds()
years_to_goal = seconds_to_goal / (365.2425 * 24 * 60 * 60)
days_to_goal = time_diff.days

# calculate progress
progress_percent = (current_value - begin_value) / (goal_value - begin_value) * 100
years_since_start = (today - deadline).days / 365.2425
annualized_return = (float(current_value) / float(begin_value)) ** (1 / years_since_start) - 1
required_return = ((float(goal_value) - float(current_value)) / float(current_value))


# check progress
if goal_type == "amount":
    if current_value >= goal_value:
        print("\nYou met your goal. The portfolio is now valued at $", str(current_value)+"!")
    else:
        print("\nYou are $"+ str(goal_value - current_value), "away from the goal.")
        print("Check out the details: \n")
        progress_print()
if goal_type == "percent":
    if annualized_return >= goal_percent:
        print("\nYou are on track with your goal with an annualzied return of", str(annualized_return)+"%!")
    else: 
        print("\n You are"+ str(goal_percent - annualized_return)+"%","below your target return.")
        print("Check out the details: \n")
        progress_print()










