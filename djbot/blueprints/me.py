import json

from flask import Blueprint, jsonify, request
from djbot.models.models import *

bp = Blueprint('me', __name__, url_prefix='/me')


# 새로운 토큰을 등록
@bp.route('/tokens', methods=['POST'])
def register():
    result = {
        "status": "Failed"
    }

    content = json.loads(request.data.decode("utf-8"))
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
    # 기존 토큰 삭제
    delete_token(content['account_id'], content['fcm_token'])

    # 새로운 토큰 등록
    add_token(content['account_id'], content['new_token'])

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


# 토큰을 추가합니다.
def add_token(account_id, token):
    fcm_token = FcmToken(account_id=account_id, token=token)
    db.session.add(fcm_token)
    db.session.commit()


# 토큰을 삭제합니다.
def delete_token(account_id, token):
    tokens = FcmToken.query.filter(FcmToken.account_id == account_id, FcmToken.token == token).all()
    for token in tokens:
        db.session.delete(token)
    db.session.commit()
