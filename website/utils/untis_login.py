import webuntis
from flask import session as flask_session
from flask_login import current_user
from webuntis import Session as UntisSession


def login():
    print("Logging into Untis...")
    if current_user.is_authenticated and current_user.untis_login != None:
        credentials = current_user.untis_login
        local_session : UntisSession = None
        try:
            local_session = UntisSession(
            server=credentials["server"],
            username = credentials["user"],
            password = credentials["password"],
            school=credentials["school"],
            useragent="Matts Demo App backend"
            )
        except webuntis.errors.BadCredentialsError:
            print("Untiis Login Failed")
            raise Exception("Send help. No Valid credentials for Untis")
        print("Logged into Untis successfully")
        return local_session.login()
    else:
        raise AttributeError("Please Login.")

def logout(session):
    session.logout()
    print("logged out of Untis")