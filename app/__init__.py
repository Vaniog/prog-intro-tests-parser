from flask import Flask
from app.config import Config
from app.extensions import db
from app.extensions import migrate
import app.main.utils as utils


def create_app(config_obj=Config()):
    app = Flask(__name__)
    app.config.from_object(config_obj)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


from app.main import routes
