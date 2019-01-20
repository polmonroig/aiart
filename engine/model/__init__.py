import logging
from flask import Flask
from . import database


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Setup the data model
    with app.app_context():
        database.init_app(app)

    # Register CRUD blueprint
    from .crud import crud
    app.register_blueprint(crud)

    # Add an error handler. Disable the output of exception for production applications
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    @app.errorhandler(Exception)
    def base_error(e):
        return """
            Application error: {}
            """.format(e), 500

    return app
