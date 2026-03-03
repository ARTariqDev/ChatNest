from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'All fields are required'}), 400

    if User.get_by_email(data['email']):
        return jsonify({'error': 'Email already registered'}), 400

    if User.get_by_username(data['username']):
        return jsonify({'error': 'Username taken'}), 400

    user = User.create(data['username'], data['email'], data['password'])
    login_user(user)
    return jsonify({'user': user.to_dict()}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400

    user = User.get_by_email(data['email'])
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    login_user(user, remember=data.get('remember', False))
    return jsonify({'user': user.to_dict()}), 200


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'ok': True}), 200


@auth_bp.route('/me')
@login_required
def me():
    return jsonify({'user': current_user.to_dict()}), 200


@auth_bp.route('/check')
def check():
    if current_user.is_authenticated:
        return jsonify({'authenticated': True, 'user': current_user.to_dict()})
    return jsonify({'authenticated': False})
