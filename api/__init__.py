import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from config import config


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_DSN

db = SQLAlchemy(app)

formatter = logging.Formatter(
    "[%(asctime)s] [%(pathname)s:%(lineno)d] %(levelname)s - %(message)s")

file_handler = RotatingFileHandler(config.LOG_FILE, maxBytes=10000000, backupCount=5)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

app.logger.addHandler(file_handler)

logger = app.logger