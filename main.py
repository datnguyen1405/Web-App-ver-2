from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import time
import requests
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

users = [{'username': 'user', 'password': generate_password_hash('password')}]

def timestamp_to_datetime(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

app.jinja_env.filters['timestamp_to_datetime'] = timestamp_to_datetime
def get_price_data(symbol):
    to_time = round(time.time())
    from_time = to_time - 0.5 * 180 * 86400
    response = requests.get(
        f"https://chart.vnsc.vn/tradingview/history?symbol={symbol}&resolution=1D&from={from_time}&to={to_time}",
        headers={}, data={})
    return response.json()

@app.route('/')
def index():
    return render_template('index_fo_login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = next((user for user in users if user['username'] == username), None)

        if user and check_password_hash(user['password'], password):
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))

        flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' in session:
        price_data = None  # Initialize to None
        if request.method == 'POST':
            symbol = request.form['symbol']
            target_return = request.form['target_return']
            price_data = get_price_data(symbol)
            # Print price_data to the console for debugging
            print(price_data)
            # Process the price_data as needed based on the target_return
            flash(f'Price information for {symbol} obtained. Target return: {target_return}%', 'success')

        return render_template('dashboard.html', username=session['user'], price_data=price_data)

    flash('You need to login first.', 'warning')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logout successful!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
