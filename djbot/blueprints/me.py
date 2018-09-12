import json

from flask import Blueprint, jsonify, request

from djbot.controllers.data import delete_token, add_token
from djbot.models.models import *

bp = Blueprint('me', __name__, url_prefix='/me')


#   #   #   #   #   #
#     사용자 정보     #
#   #   #   #   #   #
# 닉네임 변경
@bp.route('/names', methods=['PUT'])
def update_name():
    result = {
        "status": "Failed"
    }
    content = json.loads(request.data.decode("utf-8"))
    account = Account.query.filter(Account.id == content['account_id'])
    account.name = content['new_name']
    db.session.commit()

    result = {
        "status": "Success"
    }
    return json.dumps(result)


# 챗봇 캐릭터 변경
@bp.route('/bots', methods=['PUT'])
def update_bots():
    result = {
        "status": "Failed"
    }
    content = json.loads(request.data.decode("utf-8"))
    account = Account.query.filter(Account.id == content['account_id'])
    account.bot_type = content['new_bot_type']
    db.session.commit()

    result = {
        "status": "Success"
    }
    return json.dumps(result)


# 시간 변경
@bp.route('/times', methods=['PUT'])
def update_times():
    result = {
        "status": "Failed"
    }
    content = json.loads(request.data.decode("utf-8"))
    account = Account.query.filter(Account.id == content['account_id'])
    account.notify_time = content['new_notify_time']
    account.ask_time = content['new_ask_time']
    db.session.commit()

    result = {
        "status": "Success"
    }
    return json.dumps(result)

#   #   #   #   #   #
#       토큰        #
#   #   #   #   #   #
# 새로운 토큰을 등록
@bp.route('/tokens', methods=['POST'])
def register():
    result = {
        "status": "Failed"
    }

    content = json.loads(request.data.decode("utf-8"))

    tokens = FcmToken.query\
        .filter(FcmToken.account_id == content['account_id'], FcmToken.token == content['fcm_token'])\
        .all()

    if len(tokens) <= 0:
        add_token(content['account_id'], content['fcm_token'])

    result = {
        "status": "Success"
    }
    return json.dumps(result)


# 토큰을 업데이트
@bp.route('/tokens', methods=['PUT'])
def update():
    result = {
        "status": "Failed"
    }
    content = json.loads(request.data.decode("utf-8"))

    token = FcmToken.query\
        .filter(FcmToken.account_id == content['account_id'], FcmToken.token == content['fcm_token'])

    token.token = content['new_token']
    db.session.commit()

    result = {
        "status": "Success"
    }

    return json.dumps(result)


# 토큰 해제
@bp.route('/tokens/<int:account_id>/<string:fcm_token>', methods=['DELETE'])
def release(account_id, fcm_token):
    result = {
        "status": "Failed"
    }
    delete_token(account_id, fcm_token)
    result = {
        "status": "Success"
    }
    return json.dumps(result)

