"""Initialize the Insta4288 tutorial application."""
import flask

app = flask.Flask(__name__)
app.config.from_object('insta4288.config')
app.config.from_envvar('INSTA4288_SETTINGS', silent=True)

import insta4288.views  # noqa: E402  pylint: disable=wrong-import-position
import insta4288.model  # noqa: E402  pylint: disable=wrong-import-position
