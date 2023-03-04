# Investment Dashboard
Investment Dashboard is a Python-based financial management program that combines a budgeting and transaction tracking app with an investment dashboard. The program is built with Python, Flask, SQL, and PostgreSQL. It enables users to create personalized budgets and track spending by category, subcategory, and date. Transactions can be entered either as they occur or periodically, making it easy to track spending and identify areas for improvement. The program also generates comprehensive reports that enable users to compare their budgets with actual spending, making it easy to stay on top of their finances. The investment dashboard provides features like creating watchlists, querying yfinance and FRED, and getting headlines for companies on their watchlist. Additionally, the dashboard enables users to set and track goals of positions and see real-time data of holdings. Security is a top priority, and the program is designed to keep user data safe and confidential. Overall, Investment Dashboard will be an ideal tool for anyone looking to take control of their finances and investments.

## Features and Functionality
### Budgeting and Transaction Tracking
- Create a budget by category, subcategory, and date range
- Add transactions and track them by category, subcategory, and date
- Compare transactions to budgets across categories, subcategories, and/or dates to see how well you're sticking to your budget
- Edit and delete budgets and transactions as needed
- View reports that summarize budget and transaction history
- Ability to customize budget categories and subcategories to match your unique needs and preferences
- Helps users track their spending and stick to a budget, reducing financial stress and improving financial stability
- Provides a clear overview of spending patterns, helping users identify areas where they can cut back and save money
- Makes it easy to plan for future expenses and set financial goals, helping users achieve their financial objectives more efficiently
- Simplifies the process of tracking expenses and creating budgets, saving time and reducing the hassle of manual record-keeping
- Enables users to make more informed financial decisions by providing real-time feedback on their spending habits

### Investment Dashboard
- Create watchlists of stocks to track
- Query yfinance and FRED for financial data
- Get news headlines for watched stocks
- Set and track multiple goals for positions
- Real-time data of portfolio(s) holdings

## Technologies Used
### Backend
- Flask
- Python
- SQLAlchemy
- Alembic
### Frontend
- None (coming in future versions)
### Database
- SQL and PostgreSQL
### API Testing
- Flask
- Insomnia
### Other Tools
- JSON
- VS Code
- Git
### API Endpoints
| Endpoint | Method | Description |
| -------- | ------ | ----------- |
| http://localhost:5000/users | GET | Returns index of users |
| http://localhost:5000/users/:id | GET | Returns a specfic user by ID |
| http://localhost:5000/users | POST | Adds a new user |
| http://localhost:5000/users/:id | PUT | Updates all fields of a specific user by ID |
| http://localhost:5000/users/:id | PATCH | Updates provided fields of a specific user by ID |
| http://localhost:5000/users/:id | DELETE | Deletes a specific user by ID |
| http://localhost:5000/budget_items | GET | Returns index of budget items |
| http://localhost:5000/budget_items/:id | GET | Returns a specific budget item by ID|
| http://localhost:5000/budget_items/ | POST | Creates a budget item |
| http://localhost:5000/budget_items/:id | PUT | Updates all fields of a budget item by ID |
| http://localhost:5000/budget_items/:id | PATCH | Updates provided fields of a budget item by ID |
| http://localhost:5000/budget_items/:id | DELETE | Deletes a specfic budget item by ID |
| http://localhost:5000/transactions | GET | Returns index of transactions |
| http://localhost:5000/transactions/:id | GET | Returns a specfic transaction by ID |
| http://localhost:5000/transactions | POST | Adds a new transaction |
| http://localhost:5000/transactions/:id | PUT | Updates all fields of a specific transaction by ID |
| http://localhost:5000/transactions/:id | PATCH | Updates provided fields of a specific transaction by ID |
| http://localhost:5000/transactions/:id | DELETE | Deletes a specific transaction by ID |
| http://localhost:5000/categories | GET | Returns index of categories |
| http://localhost:5000/categories/:id | GET | Returns a specific category by ID |
| http://localhost:5000/categories | POST | Adds a new category |
| http://localhost:5000/subcategories | GET | Returns index of subcategories |
| http://localhost:5000/subcategories/:id | GET | Returns a specific subcategory by ID |
| http://localhost:5000/subcategories | POST | Adds a new subcategory |

### Contribution Guidelines: 
Thank you for your interest in contributing to Investment Dashboard! As this is a personal project for a programming class, contributions are not being accepted but feedback and input on features and functions are helpful. 

### Future Development
##### Branding
- Find a name that better describes the app's overall features
##### Security
- Create login functionality and ensure endpoints for web version include authentication
- Create limitations to user privileges for security and data reliability   
- Implement put and patch methods for categories and subcategories with approprite limitations for admin and users
##### Front-End 
- Develop front-end for Investment Dashboard
##### Features
- Implement the ability to export data to a CSV or PDF file for users to download
- Integrate with third-party financial services to allow users to import financial data
- Add families or groups so households can track budgets according to shared needs
- Add features for assets to track owned assets, values, income and distributions
- Add currencies to allow for multi-national use
- Add features for business / organizational use
##### User Experience
- Improve the overall design to make Investment Dashboard more visually appealing and user-friendly
- Provide tutorials or tips for users
- Implement in-app guidance to help users navigate Investment Dashboard
- Change queries to functions and add new functions for appropriate use cases
- Visualization
##### Performance and Scalability
- Optimize the back-end code for better performance and scalability
- Consider implementing techniques to improve application speed and reduce server load
- Evaluate Investment Dashboard's infrastructure to ensure it can handle increased traffic and usage
##### Testing and Quality Assurance
- Develop automated tests to ensure that Investment Dashboard functions as expected and to catch bugs early
- Conduct regular testing to ensure that Investment Dashboard is user-friendly and free of defects
