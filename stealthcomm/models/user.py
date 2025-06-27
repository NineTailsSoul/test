# models/user.py

from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    recovery_key = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    ip_address = db.Column(db.String(45), nullable=True)
    public_key = db.Column(db.Text, nullable=True)
    private_key_encrypted = db.Column(db.Text, nullable=True)

    # ✅ Friends list (comma-separated usernames)
    friends = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def find_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def authenticate_admin(username, password):
        user = User.query.filter_by(username=username, is_admin=True).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def recover_admin_account(username, recovery_key):
        return User.query.filter_by(
            username=username, is_admin=True, recovery_key=recovery_key
        ).first()

    # ✅ MUTUAL friend add method
    @staticmethod
    def add_friend(user_id, friend_username):
        user = User.find_by_id(user_id)
        friend = User.find_by_username(friend_username)

        if not user or not friend:
            return False, "User not found."

        if user.username == friend_username:
            return False, "You cannot add yourself."

        # Update user's list
        user_friends = (user.friends or "").split(",")
        if friend.username not in user_friends:
            user_friends.append(friend.username)
            user.friends = ",".join(set(filter(None, user_friends)))

        # Update friend's list
        friend_friends = (friend.friends or "").split(",")
        if user.username not in friend_friends:
            friend_friends.append(user.username)
            friend.friends = ",".join(set(filter(None, friend_friends)))

        db.session.commit()
        return True, "Friend added successfully!"
