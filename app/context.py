import yaml

from flask_sqlalchemy import SQLAlchemy

db = None


def init(app):
    global db

    with open("config.yml", 'r') as f:
        try:
            app.config.update(yaml.safe_load(f))
        except yaml.YAMLError as exc:
            print(exc)

    # The SQLite URI is defined in the Flask's config file
    db = SQLAlchemy(app)
