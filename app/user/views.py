# -*- coding: utf-8 -*-
from flask import request, render_template, url_for, flash, abort, redirect
from ..models import User
from . import user as USER
from flask.ext.login import current_user, login_required, login_user, logout_user
from form import SignupForm, LoginForm

from .. import login_manager

# login
@login_manager.user_loader
def load_user(id):
    user = User.query.filter_by(id=id).first()
    return user

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('user.login'))

@USER.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    result = '';

    if request.method == 'POST' and form.validate():
        u = User.query.filter_by(email=form.email.data).first()

        if u == None:
            flash('User not exists.', 'warning')
        else:
            user = User(u.email, '', u.nick_name)
            user.id = u.id
            user.password_hash = u.password_hash
            if user.verify_password(form.password.data):
                login_user(user, remember=form.remember.data)
                # flash('Hi~ %s, you just login success.' % user.getDisplayName(), 'warning')

                return redirect(url_for('main.index'))
            else:
                flash('password incorrect', 'error')

    return render_template('login.html', title='login', form=form);

@USER.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)

    def showMessage(type):
        if type == 'success':
            flash('Your account has been created. <a class="black-text" href="{0}">write</a> a new note?'.format(url_for('note.write')), 'success')
        if type == 'exists':
            flash('This Email address is exists.', 'warning')
        if type == 'error':
            flash('Something error when save.', 'error')

    if request.method == 'POST' and form.validate():
        user = User(
            form.email.data,
            form.password.data,
            form.nick_name.data)
        result = user.create()

        showMessage(result)
        login_user(user, remember=True)

    return render_template('signup.html', title='signup', form=form)

@USER.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
