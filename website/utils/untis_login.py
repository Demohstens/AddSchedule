import webuntis
from flask import session as flask_session
from flask_login import current_user
from webuntis import Session as UntisSession

from .. import db

def check_credentials(user):
    credentials = user.get_untis_credentials()
    if credentials != None:
        try:
            session = UntisSession(
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
        except webuntis.errors.BadCredentialsError:
            user.untis_login_valid = False
            user.untis_login = None
            db.session.commit()
            print("Untiis Login Failed")
    else:
        print("please Login")

def login(user=current_user):
    print("Logging into Untis...")
    if user:
        credentials = user.get_untis_credentials()
        if credentials != None:
            session : UntisSession = None
            try:
                session = UntisSession(
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
                raise Exception("Send help. No Valid credentials for Untis")
            if user.untis_login_valid == False:
                user.untis_login_valid = True
                db.session.commit()
            flask_session["untis_session"] = session.login()
            print(flask_session["untis_session"])
            print("Logged into Untis successfully")
        raise AttributeError("User has no credentials?????????? Check json from user db")

def logout(session):
    try:
        session = flask_session.get("untis_session")
    except KeyError:
        session = session
    print("logged out of Untis")
    try:
        session.logout()
        try:
            del flask_session["untis_session"]
        except KeyError:
            pass
    except AttributeError:
        pass