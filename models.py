# -*- coding: utf-8 -*-
from flask.ext.login import UserMixin
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base, db_session
from werkzeug.security import generate_password_hash, check_password_hash
from crypt import MyCrypt

# !!! Do not show anyone else !!!
key = '1234567890abcdef'

class Note(Base, UserMixin):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content = Column(Text)
    public = Column(Boolean())
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref('notes', lazy='dynamic'))

    @staticmethod
    def getNoteById(id):
        ec = MyCrypt(key)
        note = Note.query.filter_by(id=id).first()

        if note != None and not note.public:
            note.content = ec.decrypt(note.content).decode('utf-8')

        return note

    def __init__(self, title, content, public, user):
        self.title = title
        self.content = content
        self.public = public
        self.user = user

    def gen_time(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    def encryptContent(self):
        ec = MyCrypt(key)
        if not self.public:
            self.content = ec.encrypt(self.content.encode('utf-8'))

    def create(self):
        self.gen_time()
        self.encryptContent()

        try:
            db_session.add(self)
            db_session.commit()
        except Exception, e:
            print e
            return 'error'

        return 'success'

    def update(self):
        self.updated_at = datetime.now()
        self.encryptContent()

        try:
            db_session.add(self)
            db_session.commit()
        except Exception, e:
            print e
            return 'error'

        return 'success'

    def delete(self):
        try:
            db_session.delete(self)
            db_session.commit()
        except Exception, e:
            print e
            return 'error'

        return 'success'

    def __repr__(self):
        return '<Note %r>' % self.title

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    nick_name = Column(String(25))
    email = Column(String(40), unique=True,)
    password_hash = Column(String(120))
    created_at = Column(DateTime)

    def __init__(self, email, password, nick_name):
        self.email = email
        self.password = password
        self.nick_name = nick_name

        self.gen_password()

    def exists(self, email):
        return User.query.filter_by(email=email).first() != None

    def getDisplayName(self):
        if self.nick_name != None:
            return self.nick_name
        else:
            return self.email.split('@')[0]

    def create(self):
        if self.exists(self.email):
            return 'exists'

        self.created_at = datetime.now();

        try:
            db_session.add(self)
            db_session.commit()
        except Exception, e:
            print e
            return 'error'

        return 'success'

    def gen_password(self):
        self.password_hash = generate_password_hash(self.password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.email
