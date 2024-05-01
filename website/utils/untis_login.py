import webuntis
from flask import session as flask_session
from flask_login import current_user

from .. import db

def check_credentials(user):
    credentials = user.get_untis_credentials()
    if credentials != None:
        try:
            session = webuntis.Session(
            server=credentials["server"],
            username = credentials["user"],
            password = credentials["password"],
            school=credentials["school"],
            useragent="Matts Demo App backend"
            )
            session.login()
            session.logout()
            if user.untis_login_valid == False:
                user.untis_login_valid = True
                db.session.commit()
            return True
        except webuntis.errors.BadCredentialsError:
            user.untis_login_valid = False
            user.untis_login = None
            db.session.commit()
            print("Untiis Login Failed")
            return False
    else:
        print("please Login")
        return False

def login(user=current_user):
    print("Logging into Untis...")
    if user:
        credentials = user.get_untis_credentials()
        if credentials != None:
            try:
                session = webuntis.Session(
                server=credentials["server"],
                username = credentials["user"],
                password = credentials["password"],
                school=credentials["school"],
                useragent="Matts Demo App backend"
                )
            except webuntis.errors.BadCredentialsError:
                user.untis_login_valid = False
                user.untis_login = ""
                db.session.commit()
                print("Untiis Login Failed")
            if user.untis_login_valid == False:
                user.untis_login_valid = True
                db.session.commit()
            flask_session["untis_session"] = session.login()
            print("Logged into Untis successfully")
            return True
        raise AttributeError("User has no credentials?????????? Check json from user db")

def logout(session = None):
    try:
        session = flask_session.get("untis_session")
    except KeyError:
        session = session
    print("logged out of Untis")
    try:
        session.logout()
        try:
            del flask_session["untis_session"]
            return True
        except KeyError:
            pass
        return None
    except:
        return False
