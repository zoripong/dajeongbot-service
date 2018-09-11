import json

from flask import Blueprint, jsonify, request

from djbot.controllers.message import add_message_for_new_user
from djbot.models.models import *

bp = Blueprint('user', __name__, url_prefix='/users')


@bp.route('/<int:account_type>/<string:user_id>/<string:password>')
def login(account_type, user_id, password):
    j1 = [{
        "status": "Failed",
    }]

    if account_type == 0:
        # print(str(account_type) + "/" + user_id + "/" + password)
        account = CustomAccount.query.filter(CustomAccount.user_id == user_id, CustomAccount.password == password,
                                             CustomAccount.account_type == account_type).all()
        print(len(account))
        if len(account) == 1:
            j1 = [{
                "status": "OK",
                "user_info": {
                    "id": account[0].id,
                    "bot_type": account[0].bot_type,
                    "chat_session": "preparing"
                }
            }]
        elif len(account) < 1:
            j1 = [{
                "status": "NOT EXIST",
            }]
    else:
        # TODO: 토큰이 유효한지 체크!
        # 있는지 체크하고 있으면 업데이트 없으면 그냥 리턴
        account = ApiAccount.query.filter(ApiAccount.user_id == user_id, ApiAccount.account_type == account_type).all()
        if len(account) == 1:
            if account[0].token != password:
                # 토큰이 바뀌었다면 업데이트
                new_account = ApiAccount(user_id=account[0].user_id, name=account[0].name,
                                         birthday=account[0].birthday, account_type=account[0].account_type,
                                         bot_type=account[0].bot_type, token=password)
                db.session.delete(account[0])
                db.session.add(new_account)
                db.session.commit()
            j1 = [{
                "status": "OK",
                "user_info": {
                    "id": account[0].id,
                    "bot_type": account[0].bot_type,
                    "chat_session": "preparing"
                }
            }]
        else:
            j1 = [{
                "status": "NEW_API_USER",
                "account_type": account_type,
                "token": password,
            }]

    # TODO: 성공했을 경우 SESSION
    return jsonify(j1)


@bp.route('/signup', methods=['POST'])
def signup():
    # content = request.get_json(force=True)
    print(request.data, type(request.data))
    jsonString = request.data.decode("utf-8")
    content2 = json.loads(jsonString)
    print(type(content2))
    content = content2
    # 존재하는 아이디인지 체크
    result = {
        "status": "Failed"
        # "id": content["user_id"]
    }
    # print(type(content['account_type']))
    account = Account.query.filter(Account.user_id == content['user_id'], Account.account_type == content['account_type']).all()
    if len(account) == 0:
        # 존재하지 않는 아이디라면 insert
        detail = ApiAccount(user_id=content['user_id'], name=content['name'], birthday=content['birthday'],
                            account_type=content['account_type'], bot_type=content['bot_type'], token=content['token'])

        if content['account_type'] == 0:
            detail = CustomAccount(user_id=content['user_id'], name=content['name'], birthday=content['birthday'],
                                   account_type=content['account_type'], bot_type=content['bot_type'],
                                   password=content['password'])
        db.session.add(detail)
        db.session.commit()
        new_account = Account.query.filter(Account.user_id == content['user_id'],
                                       Account.account_type == content['account_type']).all()
        result = {
            "status": "Success",
            "user_info": {
                "id": new_account[0].id,
                "user_id": new_account[0].user_id,
                "name": new_account[0].name,
                "birthday": str(new_account[0].birthday),
                "account_type": new_account[0].account_type,
                "bot_type": new_account[0].bot_type
            }
        }
        add_message_for_new_user(new_account[0].id)

    elif len(account) >= 1:
        result = {
            "status": "ExistUser"
            # "id": content["user_id"]
        }
    return json.dumps(result)
