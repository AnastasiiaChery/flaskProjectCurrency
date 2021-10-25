from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine


db = MongoEngine()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    login_manager.init_app(app)

    app.config['MONGODB_SETTINGS'] = {
        'db': 'currency_db',
        'host': 'localhost',
        'port': 27017
    }
    db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .route_links import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .tasks_scheduler import scheduler

    return app
