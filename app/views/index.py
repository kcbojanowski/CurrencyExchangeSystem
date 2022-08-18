from flask import Blueprint, render_template

bp = Blueprint('bp_index', __name__)


@bp.route('/')
def index_get():
    return render_template('index.html')
