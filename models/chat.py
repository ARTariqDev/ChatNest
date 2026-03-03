from bson.objectid import ObjectId
from extensions import mongo
from datetime import datetime

class Chat:
    def __init__(self, chat_data):
        self.id = str(chat_data['_id'])
        self.name = chat_data.get('name')
        self.slug = chat_data.get('slug')
        self.owner_id = chat_data.get('owner_id')
        self.description = chat_data.get('description', '')
        self.created_at = chat_data.get('created_at')
        self.settings = chat_data.get('settings', {})
    
    @staticmethod
    def create(name, slug, owner_id, description='', settings=None):
        """Create a new chat"""
        chat_data = {
            'name': name,
            'slug': slug,
            'owner_id': owner_id,
            'description': description,
            'created_at': datetime.utcnow(),
            'settings': settings or {
                'allow_anonymous': False,
                'moderation_enabled': False,
                'require_approval': False
            }
        }
        result = mongo.db.chats.insert_one(chat_data)
        chat_data['_id'] = result.inserted_id
        return Chat(chat_data)
    
    @staticmethod
    def get_by_id(chat_id):
        """Get chat by ID"""
        try:
            chat_data = mongo.db.chats.find_one({'_id': ObjectId(chat_id)})
            return Chat(chat_data) if chat_data else None
        except:
            return None
    
    @staticmethod
    def get_by_slug(slug):
        """Get chat by slug"""
        chat_data = mongo.db.chats.find_one({'slug': slug})
        return Chat(chat_data) if chat_data else None
    
    @staticmethod
    def get_all():
        """Get all chats"""
        chats_data = mongo.db.chats.find()
        return [Chat(chat) for chat in chats_data]
    
    @staticmethod
    def get_by_owner(owner_id):
        """Get chats by owner"""
        chats_data = mongo.db.chats.find({'owner_id': owner_id})
        return [Chat(chat) for chat in chats_data]
    
    def to_dict(self):
        """Convert chat to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'owner_id': self.owner_id,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'settings': self.settings
        }
