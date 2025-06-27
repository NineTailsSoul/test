# routes/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        login_password = request.form["login_password"]
        chat_password = request.form["chat_password"]

        if not username or not login_password or not chat_password:
            flash("All fields are required.", "danger")
            return render_template("auth/register.html")

        if User.find_by_username(username):
            flash("Username already exists.", "danger")
            return render_template("auth/register.html")

        # Create and save new user
        new_user = User(username=username, recovery_key=chat_password)
        new_user.set_password(login_password)
        new_user.save()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.find_by_username(username)

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["is_admin"] = user.is_admin
            session['chat_password'] = request.form['chat_password']
            flash("Logged in successfully!", "success")
            return redirect(url_for("chat.home"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
