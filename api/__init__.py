from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import config.rhodes as config


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_DSN

db = SQLAlchemy(app)