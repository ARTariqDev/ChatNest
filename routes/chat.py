from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.chat import Chat
import re

chat_bp = Blueprint('chat', __name__)

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

@chat_bp.route('/create', methods=['POST'])
@login_required
def create_chat():
    """Create a new chat"""
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Chat name is required'}), 400
    
    # Generate slug from name
    slug = data.get('slug') or slugify(data['name'])
    
    # Check if slug already exists
    if Chat.get_by_slug(slug):
        return jsonify({'error': 'Chat with this slug already exists'}), 400
    
    # Create chat
    chat = Chat.create(
        name=data['name'],
        slug=slug,
        owner_id=current_user.id,
        description=data.get('description', ''),
        settings=data.get('settings')
    )
    
    return jsonify({
        'message': 'Chat created successfully',
        'chat': chat.to_dict()
    }), 201

@chat_bp.route('/<slug>', methods=['GET'])
def get_chat(slug):
    """Get chat by slug"""
    chat = Chat.get_by_slug(slug)
    
    if not chat:
        return jsonify({'error': 'Chat not found'}), 404
    
    return jsonify({'chat': chat.to_dict()}), 200

@chat_bp.route('/list', methods=['GET'])
def list_chats():
    """List all chats"""
    chats = Chat.get_all()
    return jsonify({
        'chats': [chat.to_dict() for chat in chats]
    }), 200

@chat_bp.route('/my-chats', methods=['GET'])
@login_required
def my_chats():
    """Get chats owned by current user"""
    chats = Chat.get_by_owner(current_user.id)
    return jsonify({
        'chats': [chat.to_dict() for chat in chats]
    }), 200

@chat_bp.route('/<slug>/info', methods=['GET'])
def chat_info(slug):
    """Get chat info with embed code"""
    chat = Chat.get_by_slug(slug)
    
    if not chat:
        return jsonify({'error': 'Chat not found'}), 404
    
    # Generate embed code
    embed_code = f'''<iframe 
    src="http://localhost:5000/embed/{slug}/{{page_id}}" 
    width="100%" 
    height="600px" 
    frameborder="0"
    style="border: 1px solid #ddd; border-radius: 4px;">
</iframe>'''
    
    return jsonify({
        'chat': chat.to_dict(),
        'embed_code': embed_code
    }), 200
