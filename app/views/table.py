from flask import Blueprint, render_template

bp = Blueprint('bp_table', __name__)


@bp.route('/table')
def table_get():
    return render_template('table.html')
