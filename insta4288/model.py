"""Provide request-scoped SQLite connections."""
import sqlite3
import flask
import insta4288


def dict_factory(cursor, row):
    """Return a database row as a dictionary."""
    return {column[0]: row[index]
            for index, column in enumerate(cursor.description)}


def get_db():
    """Open or reuse the current application context's connection."""
    if 'sqlite_db' not in flask.g:
        connection = sqlite3.connect(
            str(insta4288.app.config['DATABASE_FILENAME']))
        connection.row_factory = dict_factory
        connection.execute('PRAGMA foreign_keys = ON')
        flask.g.sqlite_db = connection
    return flask.g.sqlite_db


@insta4288.app.teardown_appcontext
def close_db(error):
    """Commit successful requests and close their database connections."""
    connection = flask.g.pop('sqlite_db', None)
    if connection is not None:
        try:
            if error is None:
                connection.commit()
            else:
                connection.rollback()
        finally:
            connection.close()
