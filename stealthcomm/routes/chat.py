# routes/chat.py
from flask import (
    Blueprint,
    render_template,
    session,
    request,
    jsonify,
    flash,
    redirect,
    url_for,
)
from models.chat import Chat
from models.user import User
from models.message import Message

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/home")
def home():
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to access your chats.", "danger")
        return redirect(url_for("auth.login"))

    user = User.find_by_id(user_id)
    if not user:
        session.clear()
        flash("User not found.", "danger")
        return redirect(url_for("auth.login"))

    # ✅ Load friends
    friends = []
    friend_usernames = (user.friends or "").split(",")
    for f_username in friend_usernames:
        f_user = User.find_by_username(f_username.strip())
        if f_user:
            friends.append(f_user)

    # ✅ Load user's chats
    user_chats = Chat.get_user_chats(user_id)
    chats_with_details = []

    for chat in user_chats:
        other_participants = [p for p in chat.participants if p.id != user_id]
        chat_name = (
            ", ".join([p.username for p in other_participants]) or "Unknown Chat"
        )

        # Get last message
        last_msg = (
            Message.get_last_message_for_chat(chat.id)
            if hasattr(Message, "get_last_message_for_chat")
            else None
        )
        if last_msg:
            sender = User.find_by_id(last_msg.sender_id)
            last_message_content = f"Last message from {sender.username}: (Encrypted)"
        else:
            last_message_content = "No messages yet."

        chats_with_details.append(
            {
                "id": chat.id,
                "name": chat_name,
                "participants": [
                    {"id": p.id, "username": p.username} for p in chat.participants
                ],
                "last_message_preview": last_message_content,
            }
        )

    return render_template(
        "chat/index.html", current_user=user, friends=friends, chats=chats_with_details
    )


@chat_bp.route("/start_chat_with_friend/<friend_username>", methods=["POST"])
def start_chat_with_friend(friend_username):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    current_user = User.find_by_id(user_id)
    friend_user = User.find_by_username(friend_username)

    if not current_user or not friend_user:
        return jsonify({"error": "User or friend not found."}), 404

    current_friends = (current_user.friends or "").split(",")
    if friend_username not in current_friends:
        return jsonify({"error": "You are not friends with this user."}), 403

    chat = Chat.find_direct_chat(current_user.id, friend_user.id)
    if not chat:
        chat = Chat(participants=[current_user, friend_user])
        chat.save()

    return jsonify({"success": True, "chat_id": chat.id})


@chat_bp.route("/chat_view/<chat_id>")
def chat_view(chat_id):
    user_id = session.get("user_id")
    chat = Chat.find_by_id(chat_id)

    if not chat or not any(p.id == user_id for p in chat.participants):
        flash("Chat not found or unauthorized", "danger")
        return redirect(url_for("chat.home"))

    return render_template("chat/chat_view.html", chat=chat)


@chat_bp.route("/send_message/<chat_id>", methods=["POST"])
def send_message(chat_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    chat = Chat.find_by_id(chat_id)
    if not chat or not any(p.id == user_id for p in chat.participants):
        return jsonify({"success": False, "error": "Invalid chat"}), 403

    data = request.get_json()
    content = data.get("content", "").strip()

    if not content:
        return jsonify({"success": False, "error": "Message cannot be empty"}), 400

    msg = Message(sender_id=user_id, chat_id=chat_id, content=content)
    msg.save()

    return jsonify({"success": True})
