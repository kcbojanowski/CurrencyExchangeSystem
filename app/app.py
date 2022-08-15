from flask import Flask, render_template, jsonify, url_for
from werkzeug.debug import DebuggedApplication


def create_app():
    app = Flask(__name__,
                instance_relative_config=False)
    app.debug = True
    app.wsgi_app = DebuggedApplication(app.wsgi_app)

    from .views.index import bp as bp_index
    app.register_blueprint(bp_index)
    from .views.graphs import bp as bp_graphs
    app.register_blueprint(bp_graphs)
    from .views.signin import bp as bp_signin
    app.register_blueprint(bp_signin)
    from .views.login import bp as bp_login
    app.register_blueprint(bp_login)
    from .views.table import bp as bp_table
    app.register_blueprint(bp_table)
    from .views.profile import bp as bp_profile
    app.register_blueprint(bp_profile)
    app.run()
