from flask import Blueprint, jsonify

bp = Blueprint('test', __name__)


@bp.route("/")
def hello_world():
    return jsonify({"status": "Success"})


@bp.route('/ping/')
def ping():
    return "pong"
