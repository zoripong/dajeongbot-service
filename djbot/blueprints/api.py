from flask import Blueprint

from djbot import db
from djbot.models.models import Account

bp = Blueprint('api', __name__, url_prefix='/apis')


@bp.route("/hello")
def hello_world():
    return 'hello world'


@bp.route("/register")
def register():
    user = Account(user_id="test2", name="test2", birthday="2000.05.09.", account_type=1, bot_type=1)
    db.session.add(user)
    db.session.commit()

    return 'hello world'
