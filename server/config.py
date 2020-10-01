from os import environ, path
# from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
db_file = 'data/database.db'
# load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask config variables."""

    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True
    SECRET_KEY = environ.get('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
