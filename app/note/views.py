# -*- coding: utf-8 -*-
import os
from datetime import datetime
from flask import request, render_template, url_for, flash, abort, redirect, current_app, jsonify
from flask.ext.login import current_user, login_required
from flask.ext.sqlalchemy import Pagination
from werkzeug import secure_filename
from form import CreateNoteForm, EditNoteForm
from . import note as NOTE
from ..models import Note, User
from ..helper import getNoteUrl, emptyDir
from ..upload import Upload

@NOTE.route('/upload', methods=['POST'])
def upload_image():
    success = False
    msg = u'上传出错'
    file_path = ''
    filename_prefix = 'note___{0}___{1}'.format(current_user.id, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    tmp_dir = current_app.config['TMP_DIR']
    max_size = current_app.config['MAX_CONTENT_LENGTH']
    qiniu_domain = current_app.config['QINIU_DOMAIN']

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    if request.method == 'POST':
        file = request.files['file']

        if not file:
            success = False
            msg = u'空文件'
        if not allowed_file(file.filename):
            success = False
            msg = u'文件格式不支持'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            realname = filename_prefix + str('___') + filename
            abs_file_name = os.path.join(tmp_dir, realname)

            file.save(abs_file_name)
            size = os.stat(abs_file_name).st_size

            if size > max_size:
                success = false
                msg = u'文件太大，不能超过2M'
            else:
                uploader = Upload(
                    current_app.config['QN_ACCESS_KEY'],
                    current_app.config['QN_SECRET_KEY'],
                    current_app.config['QN_BUCKET_NAME']
                )
                upload_result = uploader.send_file(realname, abs_file_name)

                if upload_result:
                    success = True
                    msg = u'文件上传成功'
                    file_path = qiniu_domain + realname
                else:
                    success = False
                    msg = u'文件上传 cdn 失败，请检查 access or secret key 是否正确配置'

            # cleanup
            emptyDir(tmp_dir)
    result = dict(success=success, msg=msg, file_path=file_path)

    return jsonify(result)

@NOTE.route('/notes', defaults={'page': 1})
@NOTE.route('/page/<int:page>')
def show_public_notes(page=1):
    pagination = Note.getIndexNotes().paginate(
        page=page,
        per_page=current_app.config['NOTE_NUM_PER_PAGE'],
        error_out=True
    )

    return render_template('index.html', title='home', isHome=True,
        notes=pagination.items, pagination=pagination, page=page)

@NOTE.route('/notes/<user>', defaults={'page': 1})
@NOTE.route('/notes/<user>/page/<int:page>')
@login_required
def show_user_notes(user, page):
    if user != current_user.nick_name:
        return render_template('404.html', title='page not found')

    pagination = Note.getUserNotes(current_user.id).paginate(
        page=page,
        per_page=current_app.config['NOTE_NUM_PER_PAGE'],
        error_out=True
    )

    return render_template('index.html', title='home',
        isHome=True,
        isUserNote=True,
        notes=pagination.items, pagination=pagination, page=page)

@NOTE.route('/search')
def show_search_notes():
    page = int(request.args.get('page') or 1)
    keyword = request.args.get('keyword')

    if not keyword:
        return render_template('404.html', title='page not found')

    pagination = Note.getSearchNotes(keyword).paginate(
        page=page,
        per_page=current_app.config['NOTE_NUM_PER_PAGE'],
        error_out=True
    )

    return render_template('index.html', title='search',
        isHome=True,
        isSearch=True,
        keyword=keyword,
        notes=pagination.items, pagination=pagination, page=page);

@NOTE.route('/note/<int:id>')
def show_note(id):
    note = Note.query.filter_by(id=id).first()

    if note == None:
        return render_template('404.html', title='page not found')

    user = User.query.filter_by(id=note.user_id).first()

    return render_template('detail.html', title=note.title,
        user=user,
        note=note,
        isDetail=True)

@NOTE.route('/<user>/<int:id>')
@login_required
def show_user_note(user, id):
    note = Note.query.filter_by(id=id).first()
    note.decryptContent()

    # current user must be the note's author
    if user != current_user.nick_name or note == None:
        return render_template('404.html', title='page not found')

    return render_template('detail.html', title=note.title, note=note, isDetail=True, user=current_user)

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
        return redirect(url_for('main.index'))
    else:
        return render_template('500.html', title='delete note error')
