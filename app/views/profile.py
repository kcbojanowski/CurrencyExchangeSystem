from flask import Blueprint, render_template

bp = Blueprint('bp_profile', __name__)


@bp.route('/profile')
def profile_get():
    return render_template('profile.html')
