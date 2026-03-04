from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from bson.objectid import ObjectId
from extensions import mongo


class User(UserMixin):
    def __init__(self, data):
        self.id = str(data['_id'])
        self.username = data.get('username')
        self.email = data.get('email')
        self.pw_hash = data.get('password_hash')

    @staticmethod
    def create(username, email, password):
        doc = {
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password),
        }
        result = mongo.db.users.insert_one(doc)
        doc['_id'] = result.inserted_id
        return User(doc)

    @staticmethod
    def get_by_id(uid):
        try:
            found = mongo.db.users.find_one({'_id': ObjectId(uid)})
            return User(found) if found else None
        except:
            return None

    @staticmethod
    def get_by_email(email):
        found = mongo.db.users.find_one({'email': email})
        return User(found) if found else None

    @staticmethod
    def get_by_username(name):
        found = mongo.db.users.find_one({'username': name})
        return User(found) if found else None

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}
