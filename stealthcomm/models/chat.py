# models/chat.py

from extensions import db
from models.user import User
from sqlalchemy.orm import joinedload
from datetime import datetime
import uuid

# Association table for many-to-many relationship between Chat and User
chat_participants = db.Table(
    "chat_participants",
    db.Column("chat_id", db.String(36), db.ForeignKey("chats.id"), primary_key=True),
    db.Column("user_id", db.String(36), db.ForeignKey("users.id"), primary_key=True),
)


class Chat(db.Model):
    __tablename__ = "chats"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(
        db.String(120), nullable=True
    )  # Group chat name or null for 1-on-1
    is_group_chat = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    participants = db.relationship(
        "User",
        secondary=chat_participants,
        lazy="subquery",
        backref=db.backref("chats", lazy=True),
    )

    messages = db.relationship(
        "Message", backref="chat", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<Chat {self.id} - {self.name if self.name else "Direct Chat"}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def find_by_id(chat_id):
        return Chat.query.get(chat_id)

    @staticmethod
    def find_direct_chat(user1_id, user2_id):
        # Find non-group chat with both users
        chats = Chat.query.filter_by(is_group_chat=False).all()
        for chat in chats:
            user_ids = [user.id for user in chat.participants]
            if user1_id in user_ids and user2_id in user_ids and len(user_ids) == 2:
                return chat
        return None

    @staticmethod
    def get_user_chats(user_id):
        # Safely load user’s chat list
        user = User.query.options(joinedload(User.chats)).filter_by(id=user_id).first()
        return user.chats if user else []

    @staticmethod
    def delete_all_involving_user(user_id):
        all_chats = Chat.query.all()
        for chat in all_chats:
            participant_ids = [p.id for p in chat.participants]
            if user_id in participant_ids:
                db.session.delete(chat)
        db.session.commit()

    @staticmethod
    def get_or_create_chat(user_ids):
        existing = Chat.find_direct_chat(user_ids[0], user_ids[1])
        if existing:
            return existing

        new_chat = Chat(is_group_chat=False)
        for uid in user_ids:
            user = User.find_by_id(uid)
            if user:
                new_chat.participants.append(user)
        new_chat.save()
        return new_chat
