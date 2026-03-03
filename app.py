# dns fix -- our router can't resolve SRV records so we use google dns
import dns.resolver
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4']

from flask import Flask, render_template, jsonify, request, redirect
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/chatnest')
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True

from extensions import mongo, login_manager, cors

mongo.init_app(app)

cors_origins = os.getenv('CORS_ORIGINS', '*').split(',')
cors.init_app(app, resources={r"/*": {
    "origins": cors_origins,
    "supports_credentials": True,
    "allow_headers": ["Content-Type"],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
}})

login_manager.init_app(app)
login_manager.login_view = 'login_page'

from models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not logged in'}), 401
    return redirect('/login')

# register api routes
from routes.auth import auth_bp
from routes.chat import chat_bp
from routes.comment import comment_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(chat_bp, url_prefix='/api/chat')
app.register_blueprint(comment_bp, url_prefix='/api/comment')


# ---- pages ----

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/chat/<slug>')
def chat_detail(slug):
    return render_template('chat-detail.html')

@app.route('/embed/<chat_slug>/<page_id>')
def embed(chat_slug, page_id):
    return render_template('embed.html', chat_slug=chat_slug, page_id=page_id)

@app.route('/api/health')
def health():
    return {'status': 'ok'}

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not found'}), 404
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=os.getenv('FLASK_ENV') == 'development', port=port)
