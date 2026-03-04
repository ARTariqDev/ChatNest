# dns fix for routers that can't resolve SRV records
import dns.resolver
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4']

from flask import Flask, render_template, jsonify, request, redirect, flash
from flask_login import login_required, current_user, logout_user, login_user
from dotenv import load_dotenv
import os, re

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/chatnest')
app.config['SESSION_COOKIE_HTTPONLY'] = True

is_prod = os.getenv('FLASK_ENV') == 'production'
if is_prod:
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True
else:
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False

from extensions import mongo, login_manager, cors
from models.user import User
from models.chat import Chat


def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text.lower().strip())
    return re.sub(r'[\s_-]+', '-', text).strip('-')

mongo.init_app(app)
login_manager.init_app(app)
cors.init_app(app, resources={r"/*": {
    "origins": os.getenv('CORS_ORIGINS', '*').split(','),
    "supports_credentials": True,
    "allow_headers": ["Content-Type"],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
}})

@login_manager.user_loader
def load_user(uid):
    return User.get_by_id(uid)

@login_manager.unauthorized_handler
def no_login():
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not logged in'}), 401
    return redirect('/login')

# blueprints
from routes.auth import auth_bp
from routes.chat import chat_bp
from routes.comment import comment_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(chat_bp, url_prefix='/api/chat')
app.register_blueprint(comment_bp, url_prefix='/api/comment')

# pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        if not username or not email or not password:
            flash('All fields required', 'error')
            return redirect(request.url)
        if User.get_by_email(email):
            flash('Email taken', 'error')
            return redirect(request.url)
        if User.get_by_username(username):
            flash('Username taken', 'error')
            return redirect(request.url)
        logout_user()
        user = User.create(username, email, password)
        login_user(user)
        return redirect(request.args.get('next') or '/dashboard')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'
        user = User.get_by_email(email)
        if not user or not user.check_password(password):
            flash('Bad credentials', 'error')
            return redirect(request.url)
        logout_user()
        login_user(user, remember=remember)
        return redirect(request.args.get('next') or '/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    chats = Chat.get_by_owner(current_user.id)
    return render_template('dashboard.html', chats=chats)

@app.route('/chat/create', methods=['POST'])
@login_required
def create_chat():
    name = request.form.get('name', '').strip()
    if not name:
        flash('Name required', 'error')
        return redirect('/dashboard')
    slug = request.form.get('slug', '').strip() or slugify(name)
    if Chat.get_by_slug(slug):
        flash('Slug taken', 'error')
        return redirect('/dashboard')
    desc = request.form.get('description', '').strip()
    chat = Chat.create(name, slug, current_user.id, desc)
    return redirect('/chat/' + chat.slug)

@app.route('/chat/<slug>')
@login_required
def chat_detail(slug):
    chat = Chat.get_by_slug(slug)
    if not chat:
        flash('Chat not found', 'error')
        return redirect('/dashboard')
    is_owner = current_user.id == chat.owner_id
    return render_template('chat-detail.html', chat=chat, is_owner=is_owner)

@app.route('/chat/<slug>/edit', methods=['POST'])
@login_required
def edit_chat(slug):
    chat = Chat.get_by_slug(slug)
    if not chat or chat.owner_id != current_user.id:
        flash('Not found or not yours', 'error')
        return redirect('/dashboard')
    name = request.form.get('name', '').strip() or chat.name
    desc = request.form.get('description', '')
    chat.update(name=name, desc=desc)
    return redirect('/chat/' + chat.slug)

@app.route('/chat/<slug>/delete', methods=['POST'])
@login_required
def delete_chat(slug):
    chat = Chat.get_by_slug(slug)
    if not chat or chat.owner_id != current_user.id:
        flash('Not found or not yours', 'error')
        return redirect('/dashboard')
    chat.delete()
    return redirect('/dashboard')

@app.route('/embed/<chat_slug>/<page_id>')
def embed(chat_slug, page_id):
    return render_template('embed.html', chat_slug=chat_slug, page_id=page_id)

@app.route('/logout', methods=['POST'])
def page_logout():
    logout_user()
    return redirect('/')

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not found'}), 404
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))
