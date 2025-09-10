from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import requests
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# --- Configuration ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a-super-secret-key-that-you-should-change'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

ALPHA_VANTAGE_API_KEY = "YOUR_API_KEY_HERE"

# --- Stock List Caching ---
def get_stock_list():
    cache_file = os.path.join(basedir, 'nse_symbols.csv')
    if os.path.exists(cache_file):
        mod_time = os.path.getmtime(cache_file)
        if (datetime.now() - datetime.fromtimestamp(mod_time)).days < 1:
            print("Loading stock list from cache.")
            return pd.read_csv(cache_file)
    print("Downloading fresh stock list from Alpha Vantage...")
    url = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={ALPHA_VANTAGE_API_KEY}'
    try:
        response = requests.get(url)
        df = pd.read_csv(pd.io.common.StringIO(response.text))
        nse_df = df[df['exchange'] == 'NSE']
        nse_df[['symbol', 'name']].to_csv(cache_file, index=False)
        return nse_df[['symbol', 'name']]
    except Exception as e:
        print(f"Failed to download stock list: {e}")
        return pd.DataFrame(columns=['symbol', 'name'])

indian_stocks_df = get_stock_list()
indian_stocks_df.columns = ['Symbol', 'Name']

# --- Database Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    shares = db.Column(db.Float, nullable=False)
    avg_cost = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Main Dashboard Route ---
@app.route('/')
@login_required
def index():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    total_expenses = sum(expense.amount for expense in expenses)
    stocks = Stock.query.filter_by(user_id=current_user.id).all()
    portfolio_value = 0
    total_cost_basis = 0
    stock_data = []
    for stock in stocks:
        symbol_with_exchange = f"{stock.symbol}.NSE"
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol_with_exchange}&apikey={ALPHA_VANTAGE_API_KEY}'
        try:
            response = requests.get(url)
            data = response.json()
            if 'Global Quote' in data and '05. price' in data['Global Quote']:
                price = float(data['Global Quote']['05. price'])
                value = price * stock.shares
                cost_basis = stock.avg_cost * stock.shares
                gain_loss = value - cost_basis
                portfolio_value += value
                total_cost_basis += cost_basis
                stock_data.append({'stock': stock, 'price': price, 'value': value, 'cost_basis': cost_basis, 'gain_loss': gain_loss})
            else:
                stock_data.append({'stock': stock, 'price': 'N/A', 'value': 'N/A', 'cost_basis': 'N/A', 'gain_loss': 'N/A'})
        except Exception as e:
            print(f"Could not fetch price for {stock.symbol}: {e}")
            stock_data.append({'stock': stock, 'price': 'N/A', 'value': 'N/A', 'cost_basis': 'N/A', 'gain_loss': 'N/A'})
    total_gain_loss = portfolio_value - total_cost_basis
    return render_template('index.html', expenses=expenses, total_expenses=total_expenses, stock_data=stock_data, portfolio_value=portfolio_value, total_cost_basis=total_cost_basis, total_gain_loss=total_gain_loss)

# --- Stock Search Route ---
@app.route('/search')
@login_required
def search():
    query = request.args.get('q', '').lower()
    if query and not indian_stocks_df.empty:
        symbol_matches = indian_stocks_df[indian_stocks_df['Symbol'].str.lower().str.contains(query)]
        name_matches = indian_stocks_df[indian_stocks_df['Name'].str.lower().str.contains(query)]
        combined = pd.concat([symbol_matches, name_matches]).drop_duplicates().head(5)
        results = combined.to_dict(orient='records')
        return jsonify(results)
    return jsonify([])

# --- Authentication Routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_user = User(username=request.form['username'])
        new_user.set_password(request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- Data Modification Routes ---
@app.route('/add', methods=['POST'])
@login_required
def add_expense():
    new_expense = Expense(description=request.form['description'], amount=float(request.form['amount']), user_id=current_user.id)
    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
@login_required
def delete_expense(id):
    expense_to_delete = Expense.query.get_or_404(id)
    db.session.delete(expense_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_stock', methods=['POST'])
@login_required
def add_stock():
    symbol = request.form['symbol'].upper()
    shares = float(request.form['shares'])
    purchase_price = float(request.form['purchase_price'])
    existing_stock = Stock.query.filter_by(symbol=symbol, user_id=current_user.id).first()
    if existing_stock:
        old_total_cost = existing_stock.shares * existing_stock.avg_cost
        new_total_cost = shares * purchase_price
        total_shares = existing_stock.shares + shares
        existing_stock.avg_cost = (old_total_cost + new_total_cost) / total_shares
        existing_stock.shares = total_shares
    else:
        new_stock = Stock(symbol=symbol, shares=shares, avg_cost=purchase_price, user_id=current_user.id)
        db.session.add(new_stock)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_stock/<int:id>')
@login_required
def delete_stock(id):
    stock_to_delete = Stock.query.get_or_404(id)
    db.session.delete(stock_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

# --- Database Initialization ---
@app.cli.command('init-db')
def init_db_command():
    with app.app_context():
        db.create_all()
    print('Initialized the database.')

if __name__ == '__main__':
    app.run(debug=True)

