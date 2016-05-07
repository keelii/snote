# -*- coding: utf-8 -*-
from flask import request, render_template, url_for, flash, abort, redirect
from ..models import Note
from . import main as MAIN
from flask.ext.login import current_user
from .. import db

@MAIN.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

# Routes
@MAIN.route('/')
def index():
    if current_user.is_authenticated:
        notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.created_at.desc())
    else:
        notes = Note.query.filter_by(public=1).order_by(Note.created_at.desc())

    for note in notes:
        if not note.public:
            note.decryptContent()

    return render_template('index.html', title='home', notes=notes, isHome=True);
