# -*- coding: utf-8 -*-
from flask import request, render_template, url_for, flash, abort, redirect
from ..models import Note
from . import main as MAIN
from flask.ext.login import current_user
from .. import db

# Home
@MAIN.route('/')
def index():
    return redirect(url_for('note.show_public_notes'))

