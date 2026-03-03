# ChatNest

Embeddable comment system. Like Disqus but self-hosted with Flask and MongoDB.

Users create a "chat" (a comment forum), then embed it on any page via an iframe.
Each page gets its own thread using a page ID.

## Setup

Needs Python 3.11+ and a MongoDB instance (local or Atlas).

```
cp .env.example .env       # edit with your mongo URI and secret key
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`.

## How it works

```
/embed/{chat_slug}/{page_id}?bg=ffffff&fg=333333&accent=2563eb
```

- `chat_slug` - the forum you created (e.g. "my-blog")
- `page_id` - a unique ID per page (e.g. "post-42", a video ID, etc.)
- Color params are optional hex values (no #)

## Project structure

```
app.py              main flask app
extensions.py       mongo, login manager, cors setup
models/
  user.py           user model (signup, login, password hashing)
  chat.py           chat/forum model
  comment.py        comment model (with threading)
routes/
  auth.py           signup, login, logout, auth check
  chat.py           create/list chats
  comment.py        create/list/edit/delete comments
templates/
  embed.html        the embeddable iframe widget
  index.html        landing page
  login.html        login form
  signup.html       signup form
  dashboard.html    manage your chats
  chat-detail.html  embed code generator + color picker
```

## API

**Auth**
- `POST /api/auth/signup` - create account
- `POST /api/auth/login` - log in
- `POST /api/auth/logout` - log out
- `GET  /api/auth/check` - check if logged in

**Chats**
- `POST /api/chat/create` - new chat
- `GET  /api/chat/<slug>` - get chat
- `GET  /api/chat/my-chats` - your chats

**Comments**
- `POST /api/comment/create` - new comment
- `GET  /api/comment/<slug>/<page_id>` - get comments for a page
- `PUT  /api/comment/<id>` - edit comment
- `DELETE /api/comment/<id>` - delete comment

## Deploying to Vercel

```
npm i -g vercel
vercel login
vercel --prod
```

Set these env vars in the Vercel dashboard:
- `MONGO_URI`
- `SECRET_KEY`
- `FLASK_ENV=production`
- `CORS_ORIGINS=https://yourdomain.com`

## License

MIT
