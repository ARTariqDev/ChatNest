from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.chat import Chat
import re

chat_bp = Blueprint('chat', __name__)


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text


@chat_bp.route('/create', methods=['POST'])
@login_required
def create_chat():
    data = request.get_json()

    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400

    slug = data.get('slug') or slugify(data['name'])

    if Chat.get_by_slug(slug):
        return jsonify({'error': 'Slug already taken'}), 400

    chat = Chat.create(
        name=data['name'],
        slug=slug,
        owner_id=current_user.id,
        description=data.get('description', ''),
    )
    return jsonify({'chat': chat.to_dict()}), 201


@chat_bp.route('/<slug>')
def get_chat(slug):
    chat = Chat.get_by_slug(slug)
    if not chat:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'chat': chat.to_dict()})


@chat_bp.route('/list')
def list_chats():
    chats = Chat.get_all()
    return jsonify({'chats': [c.to_dict() for c in chats]})


@chat_bp.route('/my-chats')
@login_required
def my_chats():
    chats = Chat.get_by_owner(current_user.id)
    return jsonify({'chats': [c.to_dict() for c in chats]})
