"""Check database integrity beyond the supplied schema tests."""
import pathlib
import sqlite3
import pytest


@pytest.fixture(name="database")
def database_fixture(db_connection):
    """Load the schema and official seed data in memory."""
    for filename in ("schema.sql", "data.sql"):
        db_connection.executescript(
            (pathlib.Path("sql") / filename).read_text(encoding="utf-8"))
    return db_connection


@pytest.mark.parametrize("username", ["awdeorio", "jflinn", "michjc", "jag"])
def test_user_cascades(database, username):
    """Delete each user and ensure all dependent rows disappear."""
    owned = database.execute(
        "SELECT postid FROM posts WHERE owner = ?", (username,)).fetchall()
    database.execute("DELETE FROM users WHERE username = ?", (username,))
    for table in ("posts", "comments", "likes"):
        assert not database.execute(
            f"SELECT * FROM {table} WHERE owner = ?", (username,)).fetchall()
    assert not database.execute(
        "SELECT * FROM following WHERE username1 = ? OR username2 = ?",
        (username, username)).fetchall()
    for post in owned:
        for table in ("comments", "likes"):
            assert not database.execute(
                f"SELECT * FROM {table} WHERE postid = ?",
                (post["postid"],)).fetchall()
    assert not database.execute("PRAGMA foreign_key_check").fetchall()


@pytest.mark.parametrize("postid", [1, 2, 3, 4])
def test_post_cascades(database, postid):
    """Delete each post while retaining its owner."""
    database.execute("DELETE FROM posts WHERE postid = ?", (postid,))
    for table in ("comments", "likes"):
        assert not database.execute(
            f"SELECT * FROM {table} WHERE postid = ?", (postid,)).fetchall()
    assert len(database.execute("SELECT * FROM users").fetchall()) == 4


@pytest.mark.parametrize("table", ["users", "posts", "following", "comments", "likes"])
def test_required_values_lengths_and_timestamps(database, table):
    """Enforce required values, declared lengths, and generated timestamps."""
    columns = database.execute(f"PRAGMA table_info({table})").fetchall()
    assert all(row["created"] for row in database.execute(
        f"SELECT created FROM {table}").fetchall())
    for column in columns:
        name = column["name"]
        if column["type"] == "INTEGER" and column["pk"]:
            continue
        with pytest.raises(sqlite3.IntegrityError):
            database.execute(f"UPDATE {table} SET {name} = NULL")
        if column["type"].startswith("VARCHAR"):
            limit = int(column["type"].split("(")[1].rstrip(")"))
            with pytest.raises(sqlite3.IntegrityError):
                database.execute(
                    f"UPDATE {table} SET {name} = ?", ("x" * (limit + 1),))


def test_relationship_integrity(database):
    """Reject duplicate follow pairs and missing foreign-key targets."""
    with pytest.raises(sqlite3.IntegrityError):
        database.execute(
            "INSERT INTO following(username1, username2) "
            "VALUES ('awdeorio', 'jflinn')")
    with pytest.raises(sqlite3.IntegrityError):
        database.execute(
            "INSERT INTO likes(owner, postid) VALUES ('awdeorio', 999)")
