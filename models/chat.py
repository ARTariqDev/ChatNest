from bson.objectid import ObjectId
from extensions import mongo
from datetime import datetime


class Chat:
    def __init__(self, data):
        self.id = str(data['_id'])
        self.name = data.get('name')
        self.slug = data.get('slug')
        self.owner_id = data.get('owner_id')
        self.desc = data.get('description', '')
        self.created_at = data.get('created_at')

    @staticmethod
    def create(name, slug, owner_id, desc=''):
        doc = {
            'name': name,
            'slug': slug,
            'owner_id': owner_id,
            'description': desc,
            'created_at': datetime.utcnow(),
        }
        result = mongo.db.chats.insert_one(doc)
        doc['_id'] = result.inserted_id
        return Chat(doc)

    @staticmethod
    def get_by_slug(slug):
        found = mongo.db.chats.find_one({'slug': slug})
        return Chat(found) if found else None

    @staticmethod
    def get_by_owner(owner_id):
        rows = mongo.db.chats.find({'owner_id': owner_id})
        return [Chat(row) for row in rows]

    @staticmethod
    def get_all():
        rows = mongo.db.chats.find()
        return [Chat(row) for row in rows]

    def update(self, name=None, desc=None):
        changes = {}
        if name is not None:
            changes['name'] = name
            self.name = name
        if desc is not None:
            changes['description'] = desc
            self.desc = desc
        if changes:
            mongo.db.chats.update_one({'_id': ObjectId(self.id)}, {'$set': changes})

    def delete(self):
        mongo.db.comments.delete_many({'chat_slug': self.slug})
        mongo.db.chats.delete_one({'_id': ObjectId(self.id)})

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'owner_id': self.owner_id,
            'description': self.desc,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
