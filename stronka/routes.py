import datetime

from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from stronka import app
from stronka.forms import RegisterForm, LoginForm
from stronka.models import User
from stronka import db
from stronka.data_utils.rates import Invoice

@app.route('/')
@app.route('/home')
def home_page():
    today = str(datetime.datetime.now().date())
    date = str(datetime.datetime.now().strftime("%d %b %Y %H:%M"))
    euros = Invoice('EUR', today, 1)
    dollar = Invoice('USD', today, 1)
    funt = Invoice('GBP', today, 1)
    cad = Invoice('CAD', today, 1)
    return render_template('index.html', eur=euros,usd=dollar,funt=funt,cad=cad, today=date)


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


@app.route('/profile')
@login_required
def profile_page():
    return render_template('profile.html')


@app.route('/table')
def table_page():
    return render_template('table.html')


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))