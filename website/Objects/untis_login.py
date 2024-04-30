import webuntis
from flask_login import current_user

from .. import db

def check_credentials(user=current_user):
    if user:
            credentials = user.get_untis_credentials()
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
            except:
                user.untis_login_valid = False
                user.untis_login = ""
                db.session.commit()
                print("Untiis Login Failed")
                return False
            if user.untis_login_valid == False:
                user.untis_login_valid = True
                db.session.commit()
            return True


def login(user=current_user):
        if user:
            credentials = user.get_untis_credentials()
            try:
                session = webuntis.Session(
                server=credentials["server"],
                username = credentials["user"],
                password = credentials["password"],
                school=credentials["school"],
                useragent="Matts Demo App backend"
                )
            except:
                user.untis_login_valid = False
                user.untis_login = ""
                db.session.commit()
                print("Untiis Login Failed")
            if user.untis_login_valid == False:
                user.untis_login_valid = True
                db.session.commit()
            return session.login()


def logout(session=login()):
    print("logged out of Untis")
    try:
        session.logout()
        return True
    except:
        return False
