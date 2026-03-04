from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.comment import Comment
from models.chat import Chat

comment_bp = Blueprint('comment', __name__)


@comment_bp.route('/create', methods=['POST'])
@login_required
def create():
    data = request.get_json()
    if not data or not data.get('chat_slug') or not data.get('page_id') or not data.get('content'):
        return jsonify({'error': 'Missing fields'}), 400
    if not Chat.get_by_slug(data['chat_slug']):
        return jsonify({'error': 'Chat not found'}), 404
    comment = Comment.create(
        data['chat_slug'], data['page_id'],
        current_user.id, current_user.username,
        data['content'], data.get('parent_id')
    )
    return jsonify({'comment': comment.to_dict()}), 201


@comment_bp.route('/<chat_slug>/<page_id>')
def get_page(chat_slug, page_id):
    if not Chat.get_by_slug(chat_slug):
        return jsonify({'error': 'Chat not found'}), 404

    comments = Comment.get_by_page(chat_slug, page_id)

    # turn flat list into a tree of replies
    lookup = {}
    for comment in comments:
        item = comment.to_dict()
        item['replies'] = []
        lookup[item['id']] = item

    roots = []
    for item in lookup.values():
        parent = item['parent_id']
        if parent and parent in lookup:
            lookup[parent]['replies'].append(item)
        else:
            roots.append(item)

    return jsonify({'comments': roots, 'total': len(comments)})


@comment_bp.route('/<comment_id>', methods=['PUT'])
@login_required
def update(comment_id):
    data = request.get_json()
    if not data or not data.get('content'):
        return jsonify({'error': 'Content required'}), 400
    comment = Comment.get_by_id(comment_id)
    if not comment:
        return jsonify({'error': 'Not found'}), 404
    if comment.deleted:
        return jsonify({'error': 'Deleted'}), 400
    if comment.user_id != current_user.id:
        return jsonify({'error': 'Not yours'}), 403
    comment.update(data['content'])
    return jsonify({'comment': comment.to_dict()})


@comment_bp.route('/<comment_id>', methods=['DELETE'])
@login_required
def delete(comment_id):
    comment = Comment.get_by_id(comment_id)
    if not comment:
        return jsonify({'error': 'Not found'}), 404
    if comment.deleted:
        return jsonify({'error': 'Already deleted'}), 400
    if comment.user_id != current_user.id:
        return jsonify({'error': 'Not yours'}), 403
    comment.delete()
    return jsonify({'ok': True})


@comment_bp.route('/<comment_id>/like', methods=['POST'])
@login_required
def like(comment_id):
    comment = Comment.get_by_id(comment_id)
    if not comment:
        return jsonify({'error': 'Not found'}), 404
    liked = comment.toggle_like(current_user.id)
    return jsonify({'liked': liked, 'likes': len(comment.likes)})
