# -*- coding: utf-8 -*-
from flask import request, render_template, url_for, flash, abort, redirect, current_app
from flask.ext.login import current_user, login_required
from flask.ext.sqlalchemy import Pagination
from form import CreateNoteForm, EditNoteForm
from . import note as NOTE
from ..models import Note
from ..helper import getNoteUrl

@NOTE.route('/notes', defaults={'page': 1})
def show_public_notes(page=1):
    pagination = Note.getIndexNotes().paginate(
        page=page,
        per_page=current_app.config['NOTE_NUM_PER_PAGE'],
        error_out=True
    )

    return render_template('index.html', title='home', isHome=True,
        notes=pagination.items, pagination=pagination, page=page)

@NOTE.route('/page/<int:page>')
def show_page_note(page):
    pagination = Note.getIndexNotes().paginate(
        page=page,
        per_page=current_app.config['NOTE_NUM_PER_PAGE'],
        error_out=True
    )

    return render_template('index.html', title='home', isHome=True,
        notes=pagination.items, pagination=pagination, page=page)

@NOTE.route('/notes/<user>', defaults={'page': 1})
@login_required
def show_user_notes(user, page):
    if user != current_user.nick_name:
        return render_template('404.html', title='page not found')

    pagination = Note.getUserNotes(current_user.id).paginate(
        page=page,
        per_page=current_app.config['NOTE_NUM_PER_PAGE'],
        error_out=True
    )

    print '-'*30
    print dir(pagination.items.count)
    return render_template('index.html', title='home',
        isHome=True,
        isUserNote=True,
        notes=pagination.items, pagination=pagination, page=page);

@NOTE.route('/note/<int:id>')
def show_note(id):
    note = Note.query.filter_by(id=id).first()

    if note == None:
        return render_template('404.html', title='page not found')

    return render_template('detail.html', title=note.title, note=note, isDetail=True)

@NOTE.route('/<user>/<int:id>')
@login_required
def show_user_note(user, id):
    note = Note.query.filter_by(id=id).first()
    note.decryptContent()

    # current user must be the note's author
    if user != current_user.nick_name or note == None:
        return render_template('404.html', title='page not found')

    return render_template('detail.html', title=note.title, note=note, isDetail=True)

@NOTE.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    form = CreateNoteForm(request.form)
    if request.method == 'POST' and form.validate():
        note = Note(
            form.title.data,
            form.content.data,
            form.public.data,
            current_user
        )
        result = note.create()
        if result == 'success':
            flash(u'You`v add a new note. 「<a class="black-text" href="{0}">{1}</a>」'.format(getNoteUrl(note), form.title.data), result)
        else:
            flash('Saving with an error.', result)

    return render_template('write.html', title='write', form=form, isWrite=True)

@NOTE.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    form = EditNoteForm(request.form)
    note = Note.query.filter_by(id=id).first()
    note.decryptContent()

    # current user must be the note's author
    if note.user_id != current_user.id or note == None:
        return render_template('404.html', title='page not found')

    if request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content
        form.public.data = note.public

    if request.method == 'POST' and form.validate():
        note.title = form.title.data
        note.content = form.content.data
        note.public = form.public.data

        result = note.update()
        if result == 'success':
            flash(u'You`v edit your note. 「<a class="black-text" href="{0}">{1}</a>」'.format(getNoteUrl(note), form.title.data), result)
        else:
            flash('Saving with an error.', result)

    return render_template('write.html', title='edit', note=note, form=form, isEdit=True)

@NOTE.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    form = EditNoteForm(request.form)
    note = Note.query.filter_by(id=id).first()

    # current user must be the note's author
    if note.user_id != current_user.id or note == None:
        return render_template('404.html', title='page not found')

    result = note.delete()

    if result == 'success':
        return redirect(url_for('index'))
    else:
        return render_template('500.html', title='delete note error')
