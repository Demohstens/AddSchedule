import webuntis
import webuntis.errors
import webuntis.errors
import webuntis.errors

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

def login(user):
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
                return session.login()
            raise AttributeError("User has no credentials??????????")

def logout(session):
    print("logged out of Untis")
    try:
        session.logout()
        return True
    except:
        return False
