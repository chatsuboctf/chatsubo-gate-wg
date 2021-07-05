"""
Global Flask Application Setting

See `.flaskenv` for default settings.
 """

import os


class Config(object):
    # If not set fall back to production for safety
    ENV = os.getenv('ENV', 'production')
    FLASK_ENV = ENV
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv('FLASK_SECRET', 'changeme')

    SQLALCHEMY_DATABASE_URI = os.getenv("CHATSUBO_DATABASE_URL", "sqlite:///chatsubo-gate.db")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
