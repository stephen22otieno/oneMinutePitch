from . import auth
from .forms import RegistrationForm
from .. import db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user
from ..models import User
from .forms import LoginForm
from flask_login import login_user, logout_user, login_required
from  ..email import mail_message



@auth.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User(email=login_form.email.data, password=login_form.password.data)
        # login_form.email.remember.data
        return redirect(url_for('main.index'))

    # if login_form.validate_on_submit():
    #     user = u
    return render_template('auth/login.html',login_form = login_form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route('/register', methods= ["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/register.html', registration_form=form)
