from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.comment import Comment
from models.chat import Chat

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/create', methods=['POST'])
@login_required
def create_comment():
    """Create a new comment"""
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('chat_slug') or not data.get('page_id') or not data.get('content'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Verify chat exists
    chat = Chat.get_by_slug(data['chat_slug'])
    if not chat:
        return jsonify({'error': 'Chat not found'}), 404
    
    # Create comment
    comment = Comment.create(
        chat_slug=data['chat_slug'],
        page_id=data['page_id'],
        user_id=current_user.id,
        username=current_user.username,
        content=data['content'],
        parent_id=data.get('parent_id')
    )
    
    return jsonify({
        'message': 'Comment created successfully',
        'comment': comment.to_dict()
    }), 201

@comment_bp.route('/<chat_slug>/<page_id>', methods=['GET'])
def get_comments(chat_slug, page_id):
    """Get all comments for a page"""
    # Verify chat exists
    chat = Chat.get_by_slug(chat_slug)
    if not chat:
        return jsonify({'error': 'Chat not found'}), 404
    
    # Get comments
    comments = Comment.get_by_page(chat_slug, page_id)
    
    # Build comment tree
    comment_dict = {c.id: c.to_dict() for c in comments}
    for comment_data in comment_dict.values():
        comment_data['replies'] = []
    
    root_comments = []
    for comment_data in comment_dict.values():
        if comment_data['parent_id']:
            parent = comment_dict.get(comment_data['parent_id'])
            if parent:
                parent['replies'].append(comment_data)
        else:
            root_comments.append(comment_data)
    
    return jsonify({
        'comments': root_comments,
        'total': len(comments)
    }), 200

@comment_bp.route('/<comment_id>', methods=['PUT'])
@login_required
def update_comment(comment_id):
    """Update a comment"""
    data = request.get_json()
    
    if not data or not data.get('content'):
        return jsonify({'error': 'Content is required'}), 400
    
    comment = Comment.get_by_id(comment_id)
    
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    # Check if user owns the comment
    if comment.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    comment.update(data['content'])
    
    return jsonify({
        'message': 'Comment updated successfully',
        'comment': comment.to_dict()
    }), 200

@comment_bp.route('/<comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    """Delete a comment"""
    comment = Comment.get_by_id(comment_id)
    
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    # Check if user owns the comment
    if comment.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    comment.delete()
    
    return jsonify({'message': 'Comment deleted successfully'}), 200

@comment_bp.route('/replies/<parent_id>', methods=['GET'])
def get_replies(parent_id):
    """Get replies to a comment"""
    replies = Comment.get_replies(parent_id)
    return jsonify({
        'replies': [reply.to_dict() for reply in replies]
    }), 200
