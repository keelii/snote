# -*- coding: utf-8 -*-
from flask import Flask, Blueprint
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from helper import Helper

login_manager = LoginManager()
login_manager.login_view = 'user.login'
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    Helper.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    from .user import user as user_blueprint
    from .note import note as note_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(note_blueprint)

    return app
