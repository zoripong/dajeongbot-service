from flask import Blueprint

from djbot import db
from djbot.models.models import *
import djbot.models.models as model
import json

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


@bp.route('/user/custom/<string:id>/<string:password>')
def login(id, password):
    account = Account.query.filter_by(user_id=id).first()

    j1 = [{"user_id": account.user_id, "id": account.id}]
    return json.dumps(j1)

