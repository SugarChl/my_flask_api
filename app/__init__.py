from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
import pymysql
db = SQLAlchemy()

def create_app():
    pymysql.install_as_MySQLdb()
    app = Flask(__name__)
    db.init_app(app)
    Config.init_app(app)
    app.config.from_object(Config)

    from app.api_1_0.__init__ import config_blueprint
    config_blueprint(app)

    return app

