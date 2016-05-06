# -*- coding: utf-8 -*-
from flask import Flask, Blueprint
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

login_manager = LoginManager()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config(config_name))

    config[config_name].init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    return app