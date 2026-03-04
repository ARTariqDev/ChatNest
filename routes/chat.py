from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.chat import Chat
import re

chat_bp = Blueprint('chat', __name__)


def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text.lower().strip())
    return re.sub(r'[\s_-]+', '-', text).strip('-')


@chat_bp.route('/create', methods=['POST'])
@login_required
def create():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Name required'}), 400
    slug = data.get('slug') or slugify(data['name'])
    if Chat.get_by_slug(slug):
        return jsonify({'error': 'Slug taken'}), 400
    chat = Chat.create(data['name'], slug, current_user.id, data.get('description', ''))
    return jsonify({'chat': chat.to_dict()}), 201


@chat_bp.route('/<slug>')
def get(slug):
    chat = Chat.get_by_slug(slug)
    if not chat:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'chat': chat.to_dict()})


@chat_bp.route('/list')
def list_all():
    return jsonify({'chats': [c.to_dict() for c in Chat.get_all()]})


@chat_bp.route('/my-chats')
@login_required
def mine():
    return jsonify({'chats': [c.to_dict() for c in Chat.get_by_owner(current_user.id)]})


@chat_bp.route('/<slug>', methods=['PUT'])
@login_required
def update(slug):
    chat = Chat.get_by_slug(slug)
    if not chat:
        return jsonify({'error': 'Not found'}), 404
    if chat.owner_id != current_user.id:
        return jsonify({'error': 'Not yours'}), 403
    data = request.get_json()
    chat.update(name=data.get('name'), desc=data.get('description'))
    return jsonify({'chat': chat.to_dict()})


@chat_bp.route('/<slug>', methods=['DELETE'])
@login_required
def delete(slug):
    chat = Chat.get_by_slug(slug)
    if not chat:
        return jsonify({'error': 'Not found'}), 404
    if chat.owner_id != current_user.id:
        return jsonify({'error': 'Not yours'}), 403
    chat.delete()
    return jsonify({'ok': True})
