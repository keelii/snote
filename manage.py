#!/usr/bin/evn python
import os
from app import create_app, db
from app.models import User, Note
from flask.ext.script import Manager, Shell
from install import install_app

app = create_app(os.getenv('FLASK_CONFIG') or 'production')

manager = Manager(app)

@manager.command
def install():
    install_app(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Note=Note)

manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
