from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


def create_app():
    """Application factory."""
    app = Flask(__name__)


    # Login management
    login_manager = LoginManager()
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))


    # Load configuration
    app.config.from_object('app.config.Config')

    # Init database
    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    Bootstrap(app)
    # Register routes
    from app.routes import register_routes
    register_routes(app)

    return app
