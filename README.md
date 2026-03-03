# ChatNest - Embeddable Comment System

A lightweight, Disqus-like commenting system built with Flask and MongoDB. Easily embeddable via iframe.

## Features

- 🔐 User authentication (signup/login)
- 💬 Nested comments and replies
- 🎨 Lightweight and embeddable
- 🔄 Real-time comment loading
- 📱 Responsive design
- 🚀 Deployable on Vercel
- 💾 MongoDB for data storage

## Architecture

```
chatnest/chat="my-chat"/[page_id]

Example:
- Create a "youtube" chat collection
- Each video gets its own page_id (e.g., video-123)
- Access: /embed/youtube/video-123
```

## Project Structure

```
chatnest/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── vercel.json            # Vercel deployment config
├── models/
│   ├── user.py           # User model
│   ├── chat.py           # Chat/Forum model
│   └── comment.py        # Comment model
├── routes/
│   ├── auth.py           # Authentication routes
│   ├── chat.py           # Chat management routes
│   └── comment.py        # Comment CRUD routes
└── templates/
    └── embed.html        # Embeddable iframe template
```

## Setup Instructions

### 1. Prerequisites

- Python 3.11+
- MongoDB (local or MongoDB Atlas)
- pip package manager

### 2. Environment Setup

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
MONGO_URI=mongodb://localhost:27017/chatnest
SECRET_KEY=your-very-secret-key-here
FLASK_ENV=development
CORS_ORIGINS=http://localhost:3000,http://localhost:5000
```

### 3. Install Dependencies

```bash
# Activate virtual environment (already created)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 4. Run Development Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### 5. Test the API

**Health Check:**
```bash
curl http://localhost:5000/api/health
```

**Create a user:**
```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "password123"}'
```

**Create a chat:**
```bash
curl -X POST http://localhost:5000/api/chat/create \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"name": "My YouTube Videos", "slug": "youtube", "description": "Comments for YouTube videos"}'
```

## Embedding ChatNest

### Get Embed Code

```bash
GET /api/chat/<slug>/info
```

Returns embed code like:

```html
<iframe 
  src="http://localhost:5000/embed/youtube/video-123" 
  width="100%" 
  height="600px" 
  frameborder="0"
  style="border: 1px solid #ddd; border-radius: 4px;">
</iframe>
```

### Example Usage

```html
<!-- On your YouTube video page -->
<div id="comments">
  <iframe 
    src="https://your-chatnest.vercel.app/embed/youtube/video-xyz123" 
    width="100%" 
    height="600px">
  </iframe>
</div>
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user
- `GET /api/auth/check` - Check auth status

### Chat Management
- `POST /api/chat/create` - Create new chat
- `GET /api/chat/<slug>` - Get chat by slug
- `GET /api/chat/list` - List all chats
- `GET /api/chat/my-chats` - Get user's chats
- `GET /api/chat/<slug>/info` - Get chat info with embed code

### Comments
- `POST /api/comment/create` - Create comment
- `GET /api/comment/<chat_slug>/<page_id>` - Get page comments
- `PUT /api/comment/<comment_id>` - Update comment
- `DELETE /api/comment/<comment_id>` - Delete comment
- `GET /api/comment/replies/<parent_id>` - Get replies

## Deployment on Vercel

### 1. Install Vercel CLI

```bash
npm i -g vercel
```

### 2. Login to Vercel

```bash
vercel login
```

### 3. Deploy

```bash
vercel --prod
```

### 4. Set Environment Variables

In Vercel dashboard, add:
- `MONGO_URI` - Your MongoDB connection string
- `SECRET_KEY` - Random secret key
- `CORS_ORIGINS` - Allowed origins (comma-separated)

### 5. Update Embed URLs

After deployment, update the embed code to use your Vercel URL:
```
https://your-app.vercel.app/embed/chat-slug/page-id
```

## MongoDB Collections

### users
```json
{
  "_id": ObjectId,
  "username": "string",
  "email": "string",
  "password_hash": "string",
  "created_at": "datetime"
}
```

### chats
```json
{
  "_id": ObjectId,
  "name": "string",
  "slug": "string",
  "owner_id": "string",
  "description": "string",
  "created_at": "datetime",
  "settings": {
    "allow_anonymous": false,
    "moderation_enabled": false,
    "require_approval": false
  }
}
```

### comments
```json
{
  "_id": ObjectId,
  "chat_slug": "string",
  "page_id": "string",
  "user_id": "string",
  "username": "string",
  "content": "string",
  "parent_id": "string|null",
  "created_at": "datetime",
  "updated_at": "datetime",
  "likes": 0,
  "is_approved": true
}
```

## Security Notes

- Change `SECRET_KEY` in production
- Use HTTPS in production
- Configure CORS properly
- Use MongoDB Atlas for production database
- Add rate limiting for API endpoints
- Implement input validation and sanitization

## License

MIT
# ChatNest
