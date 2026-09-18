# CS 4288 P2 tutorial setup

By DSTBALE

This repository contains the official P2 starter files and the completed local
SQLite and Flask tutorial setup. It is a tutorial starting point, not the full
Instagram application required for P2.

## Run locally

```bash
source env/bin/activate
./bin/insta4288run
```

Open http://localhost:8000/ to see the tutorial user list.

## Fresh installation

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install -e .
./bin/insta4288db create
./bin/insta4288run
```

`create` generates a private local session key and copies the sample uploads.
The key, database, uploads, virtual environment, and AWS PEM file are ignored by Git.

## Database commands

- `./bin/insta4288db create`: initialize; refuses to overwrite an existing database.
- `./bin/insta4288db dump`: print SQL containing the current schema and data.
- `./bin/insta4288db destroy`: delete the working database and working uploads.
- `./bin/insta4288db reset`: delete and recreate the working database and uploads.

The database contains the full P2 five-table schema and official seed data, with
required fields, length limits, generated timestamps, and cascading deletes.
Run `env/bin/pytest -q tests/db_tests` to verify it. The Flask app remains the
tutorial user list; full application tests require implementing the P2 features.

## AWS

Ubuntu 24.04 and Nginx are configured on:
`ec2-18-226-89-100.us-east-2.compute.amazonaws.com`.

```bash
ssh -i cs4288deploy.pem ubuntu@ec2-18-226-89-100.us-east-2.compute.amazonaws.com
```

Nginx proxies to localhost:8000 and protects uploaded files through
`/accounts/auth/`. Until the completed application is deployed with Gunicorn,
HTTP 502 is expected. The initial project setup explicitly postpones deployment.
The public hostname may change when the instance is stopped and started.

## Version control

```bash
git status
git pull --ff-only
# Make changes, then stage only the intended files:
git add <files>
git commit -m "Describe the change"
git push
```

Keep the GitHub repository private. You are working alone, so teammate invitation
and multi-person conflict exercises are not needed for this setup.

## Course references

- https://cumberland.isis.vanderbilt.edu/cs4288/specs/p2/
- https://cumberland.isis.vanderbilt.edu/cs4288/specs/p1/setup_git.html
- https://cumberland.isis.vanderbilt.edu/cs4288/specs/p1/setup_virtual_env.html
- https://cumberland.isis.vanderbilt.edu/cs4288/specs/p2/setup_sqlite.html
- https://cumberland.isis.vanderbilt.edu/cs4288/specs/p2/setup_flask.html
- https://cumberland.isis.vanderbilt.edu/cs4288/specs/p2/setup_aws.html
