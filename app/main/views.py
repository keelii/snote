# -*- coding: utf-8 -*-
from flask import request, render_template, url_for, flash, abort, redirect
from ..models import Note
from . import main as MAIN
from flask.ext.login import current_user
from .. import db

@MAIN.teardown_request
def shutdown_session(exception=None):
    print '----- DB Session Removed.-----'
    db.session.remove()

# Routes
@MAIN.route('/')
def index():
    return redirect(url_for('note.show_public_notes'))
