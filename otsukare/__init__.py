# coding: utf-8
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('otsukare.config.BaseConfig')

mail = Mail(app)
db = SQLAlchemy(app)

import otsukare.views

