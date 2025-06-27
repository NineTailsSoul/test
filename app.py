# app.py

from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Init Flask app
app = Flask(__name__)
app.config.from_object("config.Config")

# --- DB Setup (from extensions.py) ---
from extensions import db

db.init_app(app)

# --- Flask session ---
server_session = Session(app)

# --- SocketIO ---
socketio = SocketIO(
    app, manage_session=False, async_mode="eventlet", cors_allowed_origins="*"
)

# --- Models (import after db is ready) ---
with app.app_context():
    from models.user import User
    from models.chat import Chat
    from models.message import Message

    db.create_all()

# --- Routes ---
from routes.auth import auth_bp
from routes.chat import chat_bp
from routes.contacts import contacts_bp
from routes.admin import admin_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(chat_bp, url_prefix="/chat")
app.register_blueprint(contacts_bp, url_prefix="/contacts")
app.register_blueprint(admin_bp, url_prefix="/admin")


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("chat.home"))
    return render_template("auth/login.html")


# --- SocketIO events go here... (unchanged from your file) ---

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, debug=True, host="0.0.0.0", port=port)
