import datetime
from flask import render_template, redirect, url_for, flash, request
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
    date = str(datetime.datetime.now().strftime("%d %b %Y %H:%M"))
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
            obj_from = Wallet(user_id=current_user.id, currency_code=data['code_1'], amount=-float(data['content']))
            obj_to = Wallet(user_id=current_user.id, currency_code=data['code_2'], amount=rate)
            db.session.add(obj_from)
            db.session.commit()
            db.session.add(obj_to)
            db.session.commit()
            return '', 204
        else:
            return 'Transaction refused.', 400
    else:
        return 'Transaction refused.', 400


@app.route('/profile', )
@login_required
def profile_page_get():
    return render_template('profile.html')


@app.route('/table')
def table_page():
    date = str(datetime.datetime.now().strftime("%d %b %Y %H:%M"))
    return render_template('table.html', today=date)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))
