from flask import Blueprint, render_template

bp = Blueprint('bp_signin', __name__)


@bp.route('/signin')
def signin_get():
    return render_template('signin.html')