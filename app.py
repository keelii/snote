# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, flash, g, url_for, abort, redirect
from database import init_db, db_session
from flask.ext.login import LoginManager, current_user, login_required, login_user, logout_user
from models import User, Note
from form import SignupForm, LoginForm, CreateNoteForm, EditNoteForm

app = Flask(__name__)

app.secret_key = 'Hello Simple Note'

login_manager = LoginManager()
login_manager.init_app(app)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

# login
@login_manager.user_loader
def load_user(id):
    user = User.query.filter_by(id=id).first()
    return user

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

# Helpers
def getNoteUrl(note):
    if note.public:
        return '/note/%s' % note.id
    else:
        return '/%s/%s' % (current_user.nick_name, note.id)

@app.context_processor
def utility_processor():
    return dict(getNoteUrl=getNoteUrl)

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.created_at.desc())
    else:
        notes = Note.query.filter_by(public=1).order_by(Note.created_at.desc())

    return render_template('index.html', title='home', notes=notes, isHome=True);

@app.route('/note/<int:id>')
def show_note(id):
    note = Note.query.filter_by(id=id).first()

    if note == None:
        return render_template('404.html', title='page not found')

    return render_template('detail.html', title=note.title, note=note, isDetail=True)

@app.route('/<user>/<int:id>')
@login_required
def show_user_note(user, id):
    # note = Note.query.filter_by(id=id).first()
    note = Note.getNoteById(id)

    # current user must be the note's author
    if user != current_user.nick_name or note == None:
        return render_template('404.html', title='page not found')

    return render_template('detail.html', title=note.title, note=note, isDetail=True)


@app.route('/write', methods=['GET', 'POST'])
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
            flash(u'You`v add a new note. 「<a href="{0}">{1}</a>」'.format(getNoteUrl(note), form.title.data), result)
        else:
            flash('Saving with an error.', result)

    return render_template('write.html', title='write', form=form)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
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

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    form = EditNoteForm(request.form)
    # note = Note.query.filter_by(id=id).first()
    note = Note.getNoteById(id);

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
            flash(u'You`v edit your note. 「<a href="{0}">{1}</a>」'.format(getNoteUrl(note), form.title.data), result)
        else:
            flash('Saving with an error.', result)

    return render_template('write.html', title='edit', note=note, form=form)

@app.route('/login', methods=['GET', 'POST'])
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
                flash('Hi~ %s, you just login success.' % user.getDisplayName(), 'warning')

                return redirect(url_for('index'))
            else:
                flash('password incorrect', 'error')

    return render_template('login.html', title='login', form=form);

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)

    def showMessage(type):
        if type == 'success':
            flash('Your account has been created.', 'success')
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

    return render_template('signup.html', title='signup', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Error handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='page not found');

@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html', title='internal Server Error');

# Entry
if __name__ == '__main__':
    init_db()
    app.debug = True
    app.run()