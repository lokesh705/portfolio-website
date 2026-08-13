import os

from flask import Flask

from app.config import Config
from app.extensions import db, login_manager


def create_app(config_object: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    from app.views.admin import admin_bp
    from app.views.api import api_bp
    from app.views.public import public_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()
        _ensure_admin(app)

    return app


def _ensure_admin(app: Flask) -> None:
    from app.models import About, User

    if User.query.count() == 0:
        user = User(username=app.config["ADMIN_USERNAME"])
        user.set_password(app.config["ADMIN_PASSWORD"])
        db.session.add(user)
    if About.query.count() == 0:
        db.session.add(About())
    db.session.commit()
