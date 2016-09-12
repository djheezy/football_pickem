
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

import os
from flask_login import LoginManager

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

import views, models
