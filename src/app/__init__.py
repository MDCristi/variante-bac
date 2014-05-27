import os
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy
from config import basedir


app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000' 
app.config.from_object('config')

# login manager config
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# open Id settings
oid = OpenID(app, os.path.join(basedir, '/tmp'))

# db settings
db = SQLAlchemy(app)

from app import views
