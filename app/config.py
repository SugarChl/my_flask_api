# -*- coding: UTF-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    JSON_AS_ASCII = False
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <738763474@qq.com>'
    DB_DB = 'flask-pyjwt-auth'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:ab123@localhost/competition'

    @staticmethod
    def init_app(app):
        pass