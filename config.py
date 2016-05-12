# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

def getDatabasePath(name):
    return 'sqlite:///' + os.path.join(basedir, 'db', name)

def getTmpDir(dirname):
    return os.path.join(basedir, dirname)

class Config:
    # !!! Do not show anyone else !!!
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1234567890abcdef'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Note
    NOTE_NUM_PER_PAGE = 12

    # TMP directory
    TMP_DIR = getTmpDir('.tmp')

    MAX_CONTENT_LENGTH = os.environ.get('MAX_CONTENT_LENGTH') or 2 * 1024 * 1024

    @staticmethod
    def init_app(app):
        # maximum allowed 2 megabytes
        app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') \
        or getDatabasePath('snote-dev.db')

class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') \
        or getDatabasePath('snote-test.db')

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
        or getDatabasePath('snote.db')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}


