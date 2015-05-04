from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv('.env')

app = Flask(__name__)
db = SQLAlchemy(app)



