import datetime

from app.extensions import db
from app.main import bp
import traceback
from flask import render_template, abort, request
import app.main.utils as utils
from app.config import Config
from app.main.models import count_increment, get_count, RequestLog


@bp.route('/paradigms', methods=['POST', 'GET'])
@bp.route('/java-advanced', methods=['POST', 'GET'])
def index():
    print(Config.DATA_PATH)
    return render_template('main/index.html', names=utils.get_names(), requests_count=get_count("requests"))


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

    return utils.main(name, subject)


@bp.errorhandler(500)
def internal_error(exception):
    return traceback.format_exc()
