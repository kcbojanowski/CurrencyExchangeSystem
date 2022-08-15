from flask import Blueprint, render_template

bp = Blueprint('bp_login', __name__)


@bp.route('/login')
def login_get():
    return render_template('login.html')
