from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_cors import CORS

mongo = PyMongo()
login_manager = LoginManager()
cors = CORS()
