from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(128))

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }

class Transaction(db.Model):
    __tablename__ = 'transactions'  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(128))
    symbol = db.Column(db.String(128))
    buy_price = db.Column(db.Numeric(precision=10, scale=2))
    sell_price = db.Column(db.Numeric(precision=10, scale=2))
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    number_shares = db.Column(db.Numeric)    

    def __init__(self, amount: float, date: date, category_id: int, subcategory_id: int, user_id: int, description: str):
        self.amount = amount
        self.date = date
        self.category_id = category_id
        self.subcategory_id = subcategory_id
        self.user_id = user_id
        self.description = description

    def serialize(self):
        return {
            'id': self.id,
            'amount': str(self.amount),
            'date': self.date,
            'user_id': self.user_id,
            'description': self.description
        }

class Earnings(db.Model):
    __tablename__ = 'earnings_dates'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String(128))
    earnings_date = db.Column(db.Date)

class IndexPrices(db.Model):
    __tablename__ = 'index_prices'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String(128), unique=True)
    level = db.Column(db.Numeric(precision=10, scale=2))
    change_pct = db.Column(db.Numeric(precision=10, scale=2))

class Index(db.Model):
    __tablename__ = 'indexes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String(128))
    name = db.Column(db.String(128))

class Indicator(db.Model):
    __tablename__ = 'indicators'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String(128))
    description = db.Column(db.String(128))

class Position(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String(128))
    description = db.Column(db.String(128))     
    price = db.Column(db.Numeric(precision=10, scale=2))
    cost = db.Column(db.Numeric(precision=10, scale=2))  
    return_ = db.Column(db.Numeric(precision=10, scale=2))  
    buy_date = db.Column(db.Date)
    number_shares = db.Column(db.Numeric(precision=10, scale=2))
    dollar_return = db.Column(db.Numeric(precision=12, scale=2))
    market_value = db.Column(db.Numeric(precision=12, scale=2))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account = db.Column(db.String(128))

class StandardDeviation(db.Model):
    __tablename__ = 'standard_deviation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String(128))   
    three_year_deviation = db.Column(db.Numeric(precision=6, scale=2))
    date = db.Column(db.Date)


class WatchlistSymbols(db.Model):
    __tablename__ = 'watchlist_symbols'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String(128), unique=True)  
    etf = db.Column(db.String(4))

class UsersWatchlist(db.Model):
    __tablename__ = 'users_watchlist'
    watchlist_symbols_id = db.Column(db.Integer, db.ForeignKey('watchlist_symbols.id'), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)

class Watchlist(db.Model):
    __tablename__ = 'watchlist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String(128), unique=True) 
    price = db.Column(db.Numeric(precision=10, scale=2))
    change_pct = db.Column(db.Numeric(precision=10, scale=2))

class Goals(db.Model):
    __tablename__ = 'goals'  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goal = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(128))
    deadline = db.Column(db.Date)
    begin_value = db.Column(db.Numeric(precision=12, scale=2))
    goal_value = db.Column(db.Numeric(precision=12, scale=2))
    goal_percent = db.Column(db.Numeric(precision=10, scale=2))
    current_value = db.Column(db.Numeric(precision=12, scale=2))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
   