PRAGMA foreign_keys = ON;

CREATE TABLE users (
    username VARCHAR(20) NOT NULL PRIMARY KEY CHECK (length(username) <= 20),
    fullname VARCHAR(40) NOT NULL CHECK (length(fullname) <= 40),
    email VARCHAR(40) NOT NULL CHECK (length(email) <= 40),
    filename VARCHAR(64) NOT NULL CHECK (length(filename) <= 64),
    password VARCHAR(256) NOT NULL CHECK (length(password) <= 256),
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    postid INTEGER PRIMARY KEY AUTOINCREMENT,
    filename VARCHAR(64) NOT NULL CHECK (length(filename) <= 64),
    owner VARCHAR(20) NOT NULL CHECK (length(owner) <= 20),
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE following (
    username1 VARCHAR(20) NOT NULL CHECK (length(username1) <= 20),
    username2 VARCHAR(20) NOT NULL CHECK (length(username2) <= 20),
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (username1, username2),
    FOREIGN KEY (username1) REFERENCES users(username) ON DELETE CASCADE,
    FOREIGN KEY (username2) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE comments (
    commentid INTEGER PRIMARY KEY AUTOINCREMENT,
    owner VARCHAR(20) NOT NULL CHECK (length(owner) <= 20),
    postid INTEGER NOT NULL,
    text VARCHAR(1024) NOT NULL CHECK (length(text) <= 1024),
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner) REFERENCES users(username) ON DELETE CASCADE,
    FOREIGN KEY (postid) REFERENCES posts(postid) ON DELETE CASCADE
);

CREATE TABLE likes (
    likeid INTEGER PRIMARY KEY AUTOINCREMENT,
    owner VARCHAR(20) NOT NULL CHECK (length(owner) <= 20),
    postid INTEGER NOT NULL,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner) REFERENCES users(username) ON DELETE CASCADE,
    FOREIGN KEY (postid) REFERENCES posts(postid) ON DELETE CASCADE
);
