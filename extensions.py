from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_cors import CORS

# Initialize extensions
mongo = PyMongo()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
cors = CORS()
