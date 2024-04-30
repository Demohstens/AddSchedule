from flask import Flask
from json import load 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user



db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    
    #Import secret Key
    try:
        with open("./website/credentials.json", "r") as f:
            credentials = load(f)
            app.config["SECRET_KEY"] = credentials["secret_key"]
    except FileNotFoundError:
        app.config["SECRET_KEY"] = "asojkfoisujrefpow iu89uer 89awht p"
        app.logger.warning("Security Issue: Secret Key not safely extracted. Please fix.")

    #Database Config
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + path.join(app.instance_path, DB_NAME)
    db.init_app(app=app)


    # check Database
    from .models import User, Subject, Period

    create_database(app=app)

    migrate_database(app=app, db=db)

    # Load session user 
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app=app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    #Initialize Blueprints / links / redirects
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    @app.context_processor
    def utility_processor():
        def get_current_user():
            return current_user 
        return dict(get_current_user=get_current_user)

    return app 

def create_database(app : Flask):
    if not path.exists('sqlite:///' + app.instance_path + DB_NAME):
        with app.app_context():
            db.create_all()
            print("created Database!")

def migrate_database(app, db):
    from flask_migrate import Migrate
    migrate = Migrate(app, db)


if __name__ == "__name__":
    create_app()