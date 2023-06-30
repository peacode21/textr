from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_wtf.csrf import CSRFProtect

app = Flask(__name__,instance_relative_config=True)
#csrf = CSRFProtect(app)
#load the config
app.config.from_pyfile('config.py', silent=False)

db = SQLAlchemy(app)

#load the routes
from textr import adminroutes,userroutes,groupadminroutes