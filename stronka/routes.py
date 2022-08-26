import datetime
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from stronka import app
from stronka.forms import RegisterForm, LoginForm
from stronka.models import User
from stronka import db
from stronka.data_utils.rates import Invoice
from .models import Wallet
import requests


@app.route('/')
@app.route('/home')
def home_page():
    body = requests.get('https://api.frankfurter.app/latest?from=EUR&to=PLN')
    response = body.json()
    euros = round(response["rates"]["PLN"], 2)
    body = requests.get('https://api.frankfurter.app/latest?from=USD&to=PLN')
    response = body.json()
    dollar = round(response["rates"]["PLN"], 2)
    body = requests.get('https://api.frankfurter.app/latest?from=GBP&to=PLN')
    response = body.json()
    funt = round(response["rates"]["PLN"], 2)
    body = requests.get('https://api.frankfurter.app/latest?from=CAD&to=PLN')
    response = body.json()
    cad = round(response["rates"]["PLN"], 2)
    date = str(response["date"])
    return render_template('index.html', eur=euros, usd=dollar, funt=funt, cad=cad, today=date)


@app.route('/graphs')
def graphs_page():
    return render_template('graphs.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template('login.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        waluty = ["PLN", "GBP", "USD", "CAD"]
        for w in waluty:
            if w == "USD":
                obj_to = Wallet(user_id=current_user.id, currency_code="USD", amount=100)
            else:
                obj_to = Wallet(user_id=current_user.id, currency_code=w, amount=0)
            db.session.add(obj_to)
            db.session.commit()
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('signin.html', form=form)


@app.route('/profile', methods=['POST'])
@login_required
def profile_page():
    data = request.get_json(force=True)
    if data:
        quer = f'SELECT * FROM wallet WHERE (currency_code="{data["code_1"]}" AND user_id = "{current_user.id}");'
        wallets = db.session.execute(quer)
        amount_in_wallet = [float(t.amount) for t in wallets]
        sum_in_curr = sum(amount_in_wallet)
        if float(sum_in_curr) >= float(data['content']):
            rate_dict = requests.get(
                f"https://api.frankfurter.app/latest?amount={data['content']}&from={data['code_1']}&to={data['code_2']}").json()
            rate = float(rate_dict['rates'][data['code_2']])
            obj_from = Wallet(user_id=current_user.id, currency_code=data['code_1'], amount=-round(float(data['content']), 2))
            obj_to = Wallet(user_id=current_user.id, currency_code=data['code_2'], amount=round(rate, 2))
            db.session.add(obj_from)
            db.session.commit()
            db.session.add(obj_to)
            db.session.commit()
            return '', 204
        else:
            return 'Transaction refused.', 400
    else:
        return 'Transaction refused.', 400


@app.route('/profile')
@login_required
def profile_page_get():
    query0 = f'SELECT transaction_at FROM wallet WHERE  user_id = "{current_user.id}" AND currency_code="USD" AND amount=100;'
    starter = db.session.execute(query0)
    start_date = [i.transaction_at for i in starter]
    date = start_date[0][:10]
    rate_dict = requests.get(
        f"https://api.frankfurter.app/{date}?from=USD&to=PLN").json()
    rate = float(rate_dict['rates']['PLN'])*100
    query1 = f'SELECT currency_code FROM wallet WHERE  user_id = "{current_user.id}";'
    codes_in_wallet = db.session.execute(query1)
    currencies = list(set([i.currency_code for i in codes_in_wallet]))
    dict_wal = {}
    balance = 0
    for curr in currencies:
        quer = f'SELECT * FROM wallet WHERE (currency_code="{curr}" AND user_id = "{current_user.id}");'
        wallets = db.session.execute(quer)
        amount_in_wallet = [float(t.amount) for t in wallets]
        sum_in_curr = sum(amount_in_wallet)
        dict_wal.update({curr: round(sum_in_curr, 2)})
        if 'PLN' not in curr:
            xd = f'https://api.frankfurter.app/latest?from={curr}&to=PLN'
            body = requests.get(xd)
            response = body.json()
            value = round(response["rates"]["PLN"], 2)
        else:
            value = 1
        balance += sum_in_curr*value
    balance = round(balance, 2)
    profit = balance - rate
    query2 = f'SELECT * FROM wallet WHERE  user_id = "{current_user.id}";'
    all_transactions = db.session.execute(query2)
    history = []
    for row in all_transactions:
        history_dict = {'date': row.transaction_at[:-7], 'code': row.currency_code, 'amount': round(row.amount, 2)}
        history.append(history_dict)
    return render_template('profile.html', dict_wal=dict_wal, balance=balance, hist=history[::-1], profit=profit)


@app.route('/table')
def table_page():
    body = requests.get('https://api.frankfurter.app/latest?from=EUR&to=PLN')
    response = body.json()
    date = str(response["date"])
    return render_template('table.html', today=date)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))
