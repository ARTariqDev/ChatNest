from bson.objectid import ObjectId
from extensions import mongo
from datetime import datetime


class Chat:
    def __init__(self, data):
        self.id = str(data['_id'])
        self.name = data.get('name')
        self.slug = data.get('slug')
        self.owner_id = data.get('owner_id')
        self.description = data.get('description', '')
        self.created_at = data.get('created_at')

    @staticmethod
    def create(name, slug, owner_id, description=''):
        doc = {
            'name': name,
            'slug': slug,
            'owner_id': owner_id,
            'description': description,
            'created_at': datetime.utcnow(),
        }
        result = mongo.db.chats.insert_one(doc)
        doc['_id'] = result.inserted_id
        return Chat(doc)

    @staticmethod
    def get_by_slug(slug):
        data = mongo.db.chats.find_one({'slug': slug})
        return Chat(data) if data else None

    @staticmethod
    def get_by_owner(owner_id):
        return [Chat(c) for c in mongo.db.chats.find({'owner_id': owner_id})]

    @staticmethod
    def get_all():
        return [Chat(c) for c in mongo.db.chats.find()]

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'owner_id': self.owner_id,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
