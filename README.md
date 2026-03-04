# ChatNest

Embeddable commenting system. Drop a chat widget on any page.

Built with Flask, MongoDB Atlas, vanilla JS.

## Setup

1. Install deps:
   ```
   pip install -r requirements.txt
   ```

2. Set env vars (optional, defaults in app.py):
   ```
   MONGO_URI=mongodb+srv://...
   SECRET_KEY=something
   ```

3. Run:
   ```
   python app.py
   ```

4. Open http://localhost:5000

## How It Works

1. Sign up, log in
2. Create a chat (gives you a slug)
3. Go to chat settings, copy the embed code
4. Paste the iframe on your site

Each chat can have multiple pages (use page_id param).

## API

All JSON. Auth via session cookies.

### Auth

| Method | Path | Body | Notes |
|--------|------|------|-------|
| POST | /api/auth/signup | {username, email, password} | Creates account |
| POST | /api/auth/login | {email, password} | Logs in |
| POST | /api/auth/logout | - | Logs out |
| GET | /api/auth/check | - | Returns auth status |

### Chats

| Method | Path | Body | Notes |
|--------|------|------|-------|
| POST | /api/chat/create | {name, slug, desc} | Owner only |
| GET | /api/chat/<slug> | - | Public |
| GET | /api/chat/list | - | All chats |
| GET | /api/chat/mine | - | Your chats |
| PUT | /api/chat/<slug> | {name, desc} | Owner only |
| DELETE | /api/chat/<slug> | - | Owner only, deletes all comments too |

### Comments

| Method | Path | Body | Notes |
|--------|------|------|-------|
| POST | /api/comment/create | {chat_slug, page_id, content, parent_id} | Auth required |
| GET | /api/comment/<slug>/<page> | - | Public, returns tree |
| PUT | /api/comment/<id> | {content} | Owner only |
| DELETE | /api/comment/<id> | - | Owner only, soft delete |
| POST | /api/comment/<id>/like | - | Auth required, toggles like |

### Comment Features

- Replies: set parent_id when creating
- Likes: toggle on/off, stored as array of user IDs
- Soft delete: deleted comments show "[Comment Deleted]" but keep the reply tree
- Collapsible threads: replies can be toggled open/closed in the widget

### Embed Params

Add URL params to customize colors:

```
/embed/<slug>?page_id=home&bg=ffffff&fg=222222&accent=2563eb
```

| Param | Default | What |
|-------|---------|------|
| page_id | default | Page identifier |
| bg | ffffff | Background color (hex, no #) |
| fg | 222222 | Text color |
| accent | 2563eb | Button/link color |

## Deploy to Vercel

Has a vercel.json. Just push and connect to Vercel.

## Stack

- Flask 3.1.3
- Flask-PyMongo (MongoDB Atlas)
- Flask-Login (sessions)
- Flask-CORS (cross-origin for embeds)
- Vanilla JS, no frameworks
