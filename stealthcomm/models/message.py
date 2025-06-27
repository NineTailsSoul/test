# models/message.py
from extensions import db
from datetime import datetime
import uuid


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sender_id = db.Column(db.String(36), nullable=False)
    chat_id = db.Column(db.String(36), db.ForeignKey("chats.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_messages_for_chat(chat_id):
        return (
            Message.query.filter_by(chat_id=chat_id).order_by(Message.timestamp).all()
        )

    @staticmethod
    def get_last_message_for_chat(chat_id):
        return (
            Message.query.filter_by(chat_id=chat_id)
            .order_by(Message.timestamp.desc())
            .first()
        )

    @staticmethod
    def delete_message_by_user(message_id, user_id):
        message = Message.query.get(message_id)
        if message and message.sender_id == user_id:
            db.session.delete(message)
            db.session.commit()
            return True
        return False


@staticmethod
def create(chat_id, sender_id, content):
    from datetime import datetime

    new_msg = Message(
        chat_id=chat_id,
        sender_id=sender_id,
        content=content,
        timestamp=datetime.utcnow(),
    )
    db.session.add(new_msg)
    db.session.commit()
    return new_msg
