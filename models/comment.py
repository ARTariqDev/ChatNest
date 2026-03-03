from bson.objectid import ObjectId
from extensions import mongo
from datetime import datetime

class Comment:
    def __init__(self, comment_data):
        self.id = str(comment_data['_id'])
        self.chat_slug = comment_data.get('chat_slug')
        self.page_id = comment_data.get('page_id')
        self.user_id = comment_data.get('user_id')
        self.username = comment_data.get('username')
        self.content = comment_data.get('content')
        self.parent_id = comment_data.get('parent_id')
        self.created_at = comment_data.get('created_at')
        self.updated_at = comment_data.get('updated_at')
        self.likes = comment_data.get('likes', 0)
        self.is_approved = comment_data.get('is_approved', True)
    
    @staticmethod
    def create(chat_slug, page_id, user_id, username, content, parent_id=None):
        """Create a new comment"""
        comment_data = {
            'chat_slug': chat_slug,
            'page_id': page_id,
            'user_id': user_id,
            'username': username,
            'content': content,
            'parent_id': parent_id,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'likes': 0,
            'is_approved': True
        }
        result = mongo.db.comments.insert_one(comment_data)
        comment_data['_id'] = result.inserted_id
        return Comment(comment_data)
    
    @staticmethod
    def get_by_id(comment_id):
        """Get comment by ID"""
        try:
            comment_data = mongo.db.comments.find_one({'_id': ObjectId(comment_id)})
            return Comment(comment_data) if comment_data else None
        except:
            return None
    
    @staticmethod
    def get_by_page(chat_slug, page_id):
        """Get all comments for a specific page"""
        comments_data = mongo.db.comments.find({
            'chat_slug': chat_slug,
            'page_id': page_id,
            'is_approved': True
        }).sort('created_at', -1)
        return [Comment(comment) for comment in comments_data]
    
    @staticmethod
    def get_replies(parent_id):
        """Get all replies to a comment"""
        comments_data = mongo.db.comments.find({
            'parent_id': parent_id,
            'is_approved': True
        }).sort('created_at', 1)
        return [Comment(comment) for comment in comments_data]
    
    def update(self, content):
        """Update comment content"""
        mongo.db.comments.update_one(
            {'_id': ObjectId(self.id)},
            {'$set': {'content': content, 'updated_at': datetime.utcnow()}}
        )
        self.content = content
        self.updated_at = datetime.utcnow()
    
    def delete(self):
        """Delete comment"""
        mongo.db.comments.delete_one({'_id': ObjectId(self.id)})
    
    def to_dict(self):
        """Convert comment to dictionary"""
        return {
            'id': self.id,
            'chat_slug': self.chat_slug,
            'page_id': self.page_id,
            'user_id': self.user_id,
            'username': self.username,
            'content': self.content,
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'likes': self.likes,
            'is_approved': self.is_approved
        }
