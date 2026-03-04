# ChatNest

Embeddable commenting system. Drop a chat widget on any page.

Built with Flask, MongoDB Atlas, and vanilla JS. The main site uses server-side rendering (Jinja templates, form POSTs). The embed widget uses JS fetch calls because it runs inside an iframe on other people's sites.

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

## How it works

- Sign up, log in
- Create a chat (gives you a slug)
- Go to chat detail page, pick colors, copy the embed code
- Paste the iframe on your site

Each chat can have multiple pages (use the page ID field). So one chat can power comments on your whole blog -- just use a different page ID per post.

## Pages

The main site is all server-rendered. No JS fetch calls except in the embed widget.

- `/` -- landing page
- `/signup`, `/login` -- form POST, flash messages for errors
- `/dashboard` -- lists your chats, create/edit/delete via form POST
- `/chat/<slug>` -- chat detail with color pickers, embed code, preview
- `/embed/<slug>/<page_id>` -- the widget itself (standalone, uses JS)

## API

These endpoints exist mainly for the embed widget. All JSON, auth via session cookies.

**Auth**

- `POST /api/auth/signup` -- body: {username, email, password}
- `POST /api/auth/login` -- body: {email, password}
- `POST /api/auth/logout`
- `GET /api/auth/check` -- returns auth status

**Chats**

- `POST /api/chat/create` -- body: {name, slug, description}
- `GET /api/chat/<slug>` -- public
- `GET /api/chat/list` -- all chats
- `GET /api/chat/my-chats` -- your chats (auth required)
- `PUT /api/chat/<slug>` -- body: {name, description}, owner only
- `DELETE /api/chat/<slug>` -- owner only, deletes all comments too

**Comments**

- `POST /api/comment/create` -- body: {chat_slug, page_id, content, parent_id}
- `GET /api/comment/<slug>/<page_id>` -- returns comment tree
- `PUT /api/comment/<id>` -- body: {content}, owner only
- `DELETE /api/comment/<id>` -- owner only, soft delete
- `POST /api/comment/<id>/like` -- toggles like on/off

## Comment features

- Replies: set parent_id when creating a comment
- Likes: toggle on/off, stored as array of user IDs
- Soft delete: deleted comments show "[Comment Deleted]" but keep the reply tree intact
- Collapsible threads: replies can be toggled open/closed in the widget

## Embed colors

Add URL params to customize the widget colors:

```
/embed/<slug>/<page_id>?bg=ffffff&fg=222222&accent=2563eb
```

- `bg` -- background color (hex, no #), default ffffff
- `fg` -- text color, default 222222
- `accent` -- button/link color, default 2563eb

There are also presets on the chat detail page (Light, Dark, YouTube, Spotify, Warm, Ocean).

## Deploy

Has a vercel.json. Push to GitHub and connect to Vercel.

## Stack

- Flask 3.1.3
- Flask-PyMongo (MongoDB Atlas)
- Flask-Login (sessions)
- Flask-CORS (for the embed widget)
- Jinja2 (server-side templates)
- Flask-CORS (cross-origin for embeds)
- Vanilla JS, no frameworks
