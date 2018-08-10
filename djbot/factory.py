from flask import Flask
from werkzeug.utils import find_modules, import_string
from djbot import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://djbot:djbotAdmin2018*@119.205.221.104/DajeongBot"

    register_modules(app)
    register_blueprints(app)

    return app


def register_modules(app):
    db.init_app(app)


def register_blueprints(app):
    """Register all blueprints modules
    Reference: Armin Ronacher, "Flask for Fun and for Profit" PyBay 2016.
    """
    for name in find_modules('djbot.blueprints', include_packages=True):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)

    return None

