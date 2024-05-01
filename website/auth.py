# Dependancy imports
from flask import redirect, url_for, Blueprint, render_template, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

# Relative imports
from .models import User
from . import db   ##means from __init__.py import db
from .utils.untis_login import check_credentials
from .utils.untis_login import login as login_untis_session

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Identifier is the info used to login. Ie: Password OR Email
        identifier = request.form.get("identifier")
        password = request.form.get("password")
        # If identifier is Email
        if "@" in identifier:
            user = User.query.filter_by(email=identifier).first()
        else:
            user = User.query.filter_by(username=identifier).first()
        if user:
            if check_password_hash(user.password, password):
                # Successful Login
                login_user(user, remember=True)
                flash("Logged in successfully!", category="success")
                return redirect(request.origin or url_for("views.profile", username=user.username))
            else:
                # Failed login
                flash("Password incorrect.", category="error")
        else:
            flash("User does not exist.", category="error")
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    # Checks if a untis session exists and logs it out.
    try:
        session["untis_session"].logout()
    except KeyError:
        pass
    # Logs out of the Flask Session
    logout_user()
    return redirect("/")
    
@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        user_by_name = User.query.filter_by(username=username).first()
        # Checks if info is valid
        if user and user_by_name:
            if user.email == email:
                flash("Email already used.", category="error")
            elif user_by_name.username == username:
                flash("Username taken. Choose a different username.", category="error")
            return render_template("sign_up.html")
        elif len(email) < 4:
            flash("Email must be at least 4 characters", category="error")
        elif len(username) < 1:
            flash("Username must be at least one chatacter", category="error")
        elif not username.isalpha():
            flash("Username must be alphanumeric", category="error")
        elif len(password) < 8:
            flash("Password must be at least 8 characters", category="error")
        else:
            try:
                # User creation successful
                # Create Database entry
                new_user = User(email=email, username=username, password=generate_password_hash(password, method="pbkdf2:sha256"))
                db.session.add(new_user)
                db.session.commit()

                # Log user in
                login_user(new_user, remember=True)
                session["untis_session"] = untis_login()
                flash("Account created successfully!")
                return redirect(url_for("views.profile", username=username))
            except:
                # User Creation failed
                flash("Something went Wrong (Database). Try again or contact support.", category="error")
                return render_template("error.html", error="Database commit failed.")
        return render_template("sign_up.html")
    # If request is GET return page
    return render_template("sign_up.html")#

@auth.route("/untis-login", methods = ["GET", "POST"])
@login_required
def untis_login():
    if current_user.untis_login_valid:
        # TODO: Implement actual check if login is required.
        # This won't return an error if login info is wrong. 
        flash("Login not required.")
        return redirect("/")
    else: 
        untis_name = request.form.get("user")
        untis_password = request.form.get("password")
        untis_server = request.form.get("server")
        untis_school = request.form.get("school")
        if untis_name and untis_password and untis_server and untis_school:
            untis_string = str({"user" : untis_name, "password" : str(untis_password), "server" : untis_server, "school" : untis_school})
            current_user.untis_login = untis_string
            db.session.commit()
            flash("Untis login Added Successfully! Checking Validity... check profile for info.")
            flash(str(untis_string))
            if check_credentials(current_user) == True:
                session["untis_session"] = login_untis_session()
            return redirect("/")
        else:
            flash("Untis Login Invalid.")
            flash(str(current_user.untis_login))
            return render_template("untis_login.html")