import datetime

from app.extensions import db
from app.main import bp
import traceback
from flask import render_template, abort, request
import app.main.utils as utils
from app.config import Config


@bp.route('/', methods=['POST', 'GET'])
@bp.route('/index', methods=['POST', 'GET'])
def index():
    print(Config.DATA_PATH)
    return render_template('main/index.html', names=utils.get_names())


@bp.route('/data', methods=['GET'])
def get_data():
    data = request.args
    name = data.get('name')

    return utils.main(name)


@bp.errorhandler(500)
def internal_error(exception):
    return traceback.format_exc()
