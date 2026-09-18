"""Render the Flask tutorial's database-backed user list."""
import flask
import insta4288


@insta4288.app.route('/')
def show_index():
    """Display users other than the tutorial's example logged-in user."""
    connection = insta4288.model.get_db()
    users = connection.execute(
        'SELECT username, fullname FROM users WHERE username != ?',
        ('awdeorio',),
    ).fetchall()
    return flask.render_template('index.html', users=users)
