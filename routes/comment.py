from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.comment import Comment
from models.chat import Chat

comment_bp = Blueprint('comment', __name__)


@comment_bp.route('/create', methods=['POST'])
@login_required
def create_comment():
    data = request.get_json()

    if not data or not data.get('chat_slug') or not data.get('page_id') or not data.get('content'):
        return jsonify({'error': 'Missing fields'}), 400

    chat = Chat.get_by_slug(data['chat_slug'])
    if not chat:
        return jsonify({'error': 'Chat not found'}), 404

    comment = Comment.create(
        chat_slug=data['chat_slug'],
        page_id=data['page_id'],
        user_id=current_user.id,
        username=current_user.username,
        content=data['content'],
        parent_id=data.get('parent_id'),
    )
    return jsonify({'comment': comment.to_dict()}), 201


@comment_bp.route('/<chat_slug>/<page_id>')
def get_comments(chat_slug, page_id):
    chat = Chat.get_by_slug(chat_slug)
    if not chat:
        return jsonify({'error': 'Chat not found'}), 404

    comments = Comment.get_by_page(chat_slug, page_id)

    # build a tree: top-level comments with nested replies
    by_id = {}
    for c in comments:
        d = c.to_dict()
        d['replies'] = []
        by_id[d['id']] = d

    roots = []
    for d in by_id.values():
        if d['parent_id'] and d['parent_id'] in by_id:
            by_id[d['parent_id']]['replies'].append(d)
        else:
            roots.append(d)

    return jsonify({'comments': roots, 'total': len(comments)})


@comment_bp.route('/<comment_id>', methods=['PUT'])
@login_required
def update_comment(comment_id):
    data = request.get_json()
    if not data or not data.get('content'):
        return jsonify({'error': 'Content required'}), 400

    comment = Comment.get_by_id(comment_id)
    if not comment:
        return jsonify({'error': 'Not found'}), 404
    if comment.user_id != current_user.id:
        return jsonify({'error': 'Not yours'}), 403

    comment.update(data['content'])
    return jsonify({'comment': comment.to_dict()})


@comment_bp.route('/<comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    comment = Comment.get_by_id(comment_id)
    if not comment:
        return jsonify({'error': 'Not found'}), 404
    if comment.user_id != current_user.id:
        return jsonify({'error': 'Not yours'}), 403

    comment.delete()
    return jsonify({'ok': True})


@comment_bp.route('/replies/<parent_id>')
def get_replies(parent_id):
    replies = Comment.get_replies(parent_id)
    return jsonify({'replies': [r.to_dict() for r in replies]})
