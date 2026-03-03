from bson.objectid import ObjectId
from extensions import mongo
from datetime import datetime


class Comment:
    def __init__(self, data):
        self.id = str(data['_id'])
        self.chat_slug = data.get('chat_slug')
        self.page_id = data.get('page_id')
        self.user_id = data.get('user_id')
        self.username = data.get('username')
        self.content = data.get('content')
        self.parent_id = data.get('parent_id')
        self.created_at = data.get('created_at')

    @staticmethod
    def create(chat_slug, page_id, user_id, username, content, parent_id=None):
        doc = {
            'chat_slug': chat_slug,
            'page_id': page_id,
            'user_id': user_id,
            'username': username,
            'content': content,
            'parent_id': parent_id,
            'created_at': datetime.utcnow(),
        }
        result = mongo.db.comments.insert_one(doc)
        doc['_id'] = result.inserted_id
        return Comment(doc)

    @staticmethod
    def get_by_id(comment_id):
        try:
            data = mongo.db.comments.find_one({'_id': ObjectId(comment_id)})
            return Comment(data) if data else None
        except:
            return None

    @staticmethod
    def get_by_page(chat_slug, page_id):
        cursor = mongo.db.comments.find({
            'chat_slug': chat_slug,
            'page_id': page_id,
        }).sort('created_at', -1)
        return [Comment(c) for c in cursor]

    @staticmethod
    def get_replies(parent_id):
        cursor = mongo.db.comments.find({
            'parent_id': parent_id,
        }).sort('created_at', 1)
        return [Comment(c) for c in cursor]

    def update(self, content):
        mongo.db.comments.update_one(
            {'_id': ObjectId(self.id)},
            {'$set': {'content': content}}
        )
        self.content = content

    def delete(self):
        mongo.db.comments.delete_one({'_id': ObjectId(self.id)})

    def to_dict(self):
        return {
            'id': self.id,
            'chat_slug': self.chat_slug,
            'page_id': self.page_id,
            'user_id': self.user_id,
            'username': self.username,
            'content': self.content,
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
