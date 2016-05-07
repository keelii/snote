# -*- coding: utf-8 -*-
from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField
from wtforms.validators import Length, Required

class CreateNoteForm(Form):
    title = TextField('Title', validators=[
        Required(),
        Length(min=1, max=100)
    ])
    content = TextAreaField(' ', validators=[
        Required()
    ],  render_kw={"id": "editor"})
    public = BooleanField('Public', render_kw={"title": "Others can view."})

class EditNoteForm(Form):
    title = TextField('Title', validators=[
        Required(),
        Length(min=1, max=100)
    ])
    content = TextAreaField(' ', validators=[
        Required()
    ],  render_kw={"id": "editor"})
    public = BooleanField('Public', render_kw={"title": "Others can view."})
