# routes/admin.py

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    request,
    jsonify,
)
from models.user import User
from models.message import Message
from models.chat import Chat
from functools import wraps

admin_bp = Blueprint("admin", __name__)


# --- Admin Access Decorator ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Admin access required.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


# --- Admin Dashboard ---
@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    all_users = User.get_all_users()
    deleted_messages = Message.get_deleted_messages_for_admin()

    formatted_deleted_messages = []
    for msg in deleted_messages:
        sender = User.find_by_id(msg.sender_id)
        chat = Chat.find_by_id(msg.chat_id)

        chat_participants = []
        if chat:
            for p_id in chat.participant_ids.split(","):
                p_user = User.find_by_id(p_id.strip())
                if p_user:
                    chat_participants.append(p_user.username)

        formatted_deleted_messages.append(
            {
                "id": msg.id,
                "sender_username": sender.username if sender else "Unknown",
                "content": msg.content,
                "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "chat_participants": ", ".join(chat_participants),
            }
        )

    return render_template(
        "admin/dashboard.html",
        users=all_users,
        deleted_messages=formatted_deleted_messages,
    )


# --- Toggle Admin Status ---
@admin_bp.route("/admin/toggle_admin/<user_id>", methods=["POST"])
@admin_required
def toggle_admin_status(user_id):
    user = User.find_by_id(user_id)
    if user and user.id != session["user_id"]:
        user.is_admin = not user.is_admin
        user.save()
        flash(f"{user.username}'s admin status changed.", "success")
    else:
        flash("You cannot change your own admin status.", "danger")
    return redirect(url_for("admin.dashboard"))


# --- Recover Message ---
@admin_bp.route("/admin/recover_message/<message_id>", methods=["POST"])
@admin_required
def recover_message(message_id):
    message = Message.find_by_id(message_id)
    if message:
        message.is_deleted_by_user = False
        message.save()
        flash("Message recovered.", "success")
    else:
        flash("Message not found.", "danger")
    return redirect(url_for("admin.dashboard"))


# --- Permanently Delete Message ---
@admin_bp.route("/admin/permanent_delete_message/<message_id>", methods=["POST"])
@admin_required
def permanent_delete_message(message_id):
    message = Message.find_by_id(message_id)
    if message:
        message.delete()
        flash("Message permanently deleted.", "success")
    else:
        flash("Message not found.", "danger")
    return redirect(url_for("admin.dashboard"))


# --- Delete User & Associated Data ---
@admin_bp.route("/admin/delete_user/<user_id>", methods=["POST"])
@admin_required
def delete_user(user_id):
    if user_id == session["user_id"]:
        flash("You cannot delete yourself.", "danger")
        return redirect(url_for("admin.dashboard"))

    user = User.find_by_id(user_id)
    if user:
        # Delete associated messages
        Message.delete_all_for_user(user.id)

        # Delete chats (you can refine this logic)
        Chat.delete_all_involving_user(user.id)

        username = user.username
        user.delete()
        flash(f"User {username} and associated data deleted.", "success")
    else:
        flash("User not found.", "danger")

    return redirect(url_for("admin.dashboard"))
