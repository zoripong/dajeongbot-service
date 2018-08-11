from flask import Blueprint, request

from djbot import db
from djbot.models.models import *
import djbot.models.models as model
import json


bp = Blueprint('api', __name__, url_prefix='/apis')

# test code


@bp.route("/hello")
def hello_world():
    return 'hello world'


@bp.route("/register")
def register():
    user = Account(user_id="test2", name="test2", birthday="2000.05.09.", account_type=1, bot_type=1)
    db.session.add(user)
    db.session.commit()

    return 'hello world'


@bp.route("/join")
def join():
    user_id = 'test'
    password = 'test'
    account = Account.query.join(CustomAccount, Account.id == CustomAccount.account_id) \
        .add_columns(Account.id, Account.user_id, CustomAccount.password) \
        .filter(Account.user_id == user_id, CustomAccount.password == password) \
        .all()

    if len(account) == 1:
        return "Success"
    else:
        return "Failed"


# end of test code


@bp.route('/users/custom/<string:user_id>/<string:password>')
def login(user_id, password):
    account = Account.query.join(CustomAccount, Account.id == CustomAccount.account_id) \
        .add_columns(Account.id, Account.user_id, CustomAccount.password) \
        .filter(Account.user_id == user_id, CustomAccount.password == password) \
        .all()
    j1 = [{
        "status": "Failed",
    }]
    if len(account) == 1:
        j1 = [{
            "status": "OK",
            "user_info": {
                "id": account[0].id,
                "chat_session": "preparing"
            }
        }]
    return json.dumps(j1)


@bp.route('/signup', methods=['GET','POST'])
def signup():
    content = json.loads(json.dumps(request.json))
    print(request.get_json(force=True))
    js = request.get_json(force=True)
    j1 = {
        "status": "Success",
        "info": js['user_id']
    }

    Account.query.filter()
    user = Account(user_id="test2", name="test2", birthday="2000.05.09.", account_type=1, bot_type=1)
    db.session.add(user)
    db.session.commit()

    return json.dumps(j1)

