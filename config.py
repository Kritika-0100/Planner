import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'your_secret_key_here'
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False