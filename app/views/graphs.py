from flask import Blueprint, render_template

bp = Blueprint('bp_graphs', __name__)


@bp.route('/graphs')
def graphs_get():
    return render_template('graphs.html')
