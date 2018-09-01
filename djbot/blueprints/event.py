from flask import Blueprint, jsonify
from djbot.models.models import *

bp = Blueprint('event', __name__, url_prefix='/events')


@bp.route('/dates/<int:account_id>')
def get_dates_having_event(account_id):
    events = Event.query.filter(Event.account_id == account_id).order_by(Event.id)
    return jsonify([ event.schedule_when for event in events])


@bp.route('/<int:account_id>/<string:year>/<string:month>/<string:date>')
def get_events(account_id, year, month, date):
    date = year + "-" + month + "-" + date

    events = Event.query.filter(Event.account_id == account_id, Event.schedule_when == date).order_by(Event.id)
    return jsonify([{
        "id": event.id,
        "schedule_when": event.schedule_when,
        "schedule_where": event.schedule_where,
        "schedule_what": event.schedule_what,
        "assign_time": event.assign_time,
        "detail": event.detail,
        "review": event.review
    }for event in events])



