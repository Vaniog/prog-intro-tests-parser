import datetime

from app.extensions import db
from app.main import bp
from flask import render_template, request
import app.main.utils as utils
from app.main.models import count_increment, get_count, RequestLog


@bp.route('/', methods=['GET'])
def index():
    return render_template('main/index.html', requests_count=get_count("requests"))


@bp.route('/paradigms', methods=['GET'])
@bp.route('/java-advanced', methods=['GET'])
def tables():
    return render_template('main/tables.html', names=utils.get_names(), requests_count=get_count("requests"))


@bp.route('/data', methods=['GET'])
def get_data():
    data = request.args
    name = data.get('name')
    subject = data.get('subject')

    count_increment("requests")
    log = RequestLog(
        name=name,
        subject=subject
    )
    db.session.add(log)
    db.session.commit()

    try:
        return utils.main(name, subject)
    except utils.NotFoundStudentException as e:
        return f"[NOT FOUND] student: {name}, subject: {subject}"
    except Exception as e:
        return e
