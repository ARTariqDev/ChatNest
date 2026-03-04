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
        self.deleted = data.get('deleted', False)
        raw_likes = data.get('likes', [])
        self.likes = raw_likes if isinstance(raw_likes, list) else []

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
            'likes': [],
        }
        result = mongo.db.comments.insert_one(doc)
        doc['_id'] = result.inserted_id
        return Comment(doc)

    @staticmethod
    def get_by_id(comment_id):
        try:
            found = mongo.db.comments.find_one({'_id': ObjectId(comment_id)})
            return Comment(found) if found else None
        except:
            return None

    @staticmethod
    def get_by_page(chat_slug, page_id):
        query = {'chat_slug': chat_slug, 'page_id': page_id}
        rows = mongo.db.comments.find(query).sort('created_at', -1)
        return [Comment(row) for row in rows]

    def toggle_like(self, user_id):
        # fix old docs that stored likes as int instead of list
        current = mongo.db.comments.find_one({'_id': ObjectId(self.id)}, {'likes': 1})
        if current and not isinstance(current.get('likes'), list):
            mongo.db.comments.update_one({'_id': ObjectId(self.id)}, {'$set': {'likes': []}})
            self.likes = []

        if user_id in self.likes:
            mongo.db.comments.update_one({'_id': ObjectId(self.id)}, {'$pull': {'likes': user_id}})
            self.likes.remove(user_id)
            return False
        else:
            mongo.db.comments.update_one({'_id': ObjectId(self.id)}, {'$addToSet': {'likes': user_id}})
            self.likes.append(user_id)
            return True

    def update(self, content):
        mongo.db.comments.update_one({'_id': ObjectId(self.id)}, {'$set': {'content': content}})
        self.content = content

    def delete(self):
        mongo.db.comments.update_one({'_id': ObjectId(self.id)}, {'$set': {'deleted': True}})
        self.deleted = True

    def to_dict(self):
        info = {
            'id': self.id,
            'chat_slug': self.chat_slug,
            'page_id': self.page_id,
            'parent_id': self.parent_id,
            'deleted': self.deleted,
            'username': self.username,
            'likes': len(self.likes),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        if self.deleted:
            info['user_id'] = None
            info['content'] = None
        else:
            info['user_id'] = self.user_id
            info['content'] = self.content
            info['liked_by'] = self.likes
        return info
