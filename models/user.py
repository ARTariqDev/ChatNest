from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from bson.objectid import ObjectId
from extensions import mongo


class User(UserMixin):
    def __init__(self, data):
        self.id = str(data['_id'])
        self.username = data.get('username')
        self.email = data.get('email')
        self.password_hash = data.get('password_hash')
        self.created_at = data.get('created_at')

    @staticmethod
    def create(username, email, password):
        doc = {
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password),
            'created_at': ObjectId().generation_time,
        }
        result = mongo.db.users.insert_one(doc)
        doc['_id'] = result.inserted_id
        return User(doc)

    @staticmethod
    def get_by_id(user_id):
        try:
            data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
            return User(data) if data else None
        except:
            return None

    @staticmethod
    def get_by_email(email):
        data = mongo.db.users.find_one({'email': email})
        return User(data) if data else None

    @staticmethod
    def get_by_username(username):
        data = mongo.db.users.find_one({'username': username})
        return User(data) if data else None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
