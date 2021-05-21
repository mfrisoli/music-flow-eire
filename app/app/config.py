from os import environ, path, getenv

# SET CONFIGURATIONS IN .flaskenv -> 'development', 'testing', 'production'
config_name = getenv('FLASK_CONFIG') or 'default'

basedir = path.abspath(path.dirname(__file__))

class Config:
    SECRET_KEY = environ.get('SECRET_KEY') or 'Very hard to guess string'
      
    # Email smtp
    MAIL_SERVER = environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
    MAIL_PORT = environ.get('MAIL_PORT') or 587
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', 1]
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MUSIC_FLOW_MAIL_SUBJECT_PREFIX = '[Music-Flow]'
    MUSIC_FLOW_MAIL_SENDER = 'Music-Flow Admin <musicflow.eire@gmail.com>'
    MUSIC_FLOW_ADMIN = environ.get('MUSIC_FLOW_ADMIN') or 'musicflow.eire@gmail.com'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # Database connection & Configuration
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URL') or \
         'sqlite:///' + path.join(basedir, 'data.sqlite')


class TestingConfig(Config):
    TESTING = True
    # Database connection & Configuration
    SQLALCHEMY_DATABASE_URI = environ.get('TEST_DATABASE_URL') or \
         'sqlite:///' + path.join(basedir, 'dev-data.sqlite')


class ProductionConfig(Config):
    # Database connection & Configuration
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or \
         'sqlite:///' + path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}