from logging.handlers import RotatingFileHandler

from flask import Flask, logging
from werkzeug.utils import find_modules, import_string
from djbot import db
import config



def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    db_config = config.DATABASE_CONFIG
    uri = "mysql://" + db_config['user'] + ":" + db_config['password'] + "@" + db_config['host'] + "/" + db_config['db']
    app.config['SQLALCHEMY_DATABASE_URI'] = uri

    register_logger(app)
    register_modules(app)
    register_blueprints(app)

    return app


def register_logger(app):
    handler = RotatingFileHandler('info.log', maxBytes=10000, backupCount=1)
    app.logger.addHandler(handler)
    pass


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

