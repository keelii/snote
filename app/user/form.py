# -*- coding: utf-8 -*-
from wtforms import Form, BooleanField, TextField, TextAreaField, RadioField, PasswordField
from wtforms.validators import Length, Required, EqualTo, Email

class SignupForm(Form):
    email = TextField('Email', validators=[
        Email(),
        Required(),
        Length(min=5, max=40)
    ])
    nick_name = TextField('Nickname', validators=[
        Length(min=3, max=25),
    ])
    password = PasswordField('Password', validators=[
        Required(),
        Length(min=6, max=20),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm password')

class LoginForm(Form):
    email = TextField('Email', validators=[
        Email(),
        Required(),
        Length(min=5, max=40)
    ])
    password = PasswordField('Password', validators=[
        Required(),
        Length(min=6, max=20)
    ])
    remember = BooleanField('remember')
