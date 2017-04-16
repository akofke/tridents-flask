from os import environ


class Config:
    DEBUG = True
    PROD = False
    SECRET_KEY = 'development key'

    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AUTH0_CLIENT_ID = environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = environ.get('AUTH0_CLIENT_SECRET')
    AUTH0_DOMAIN = environ.get('AUTH0_DOMAIN')


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/tridents_dev'


class StagingConfig(Config):
    DEBUG = False
    SECRET_KEY = environ.get('SECRET_KEY')


class ProductionConfig(Config):
    DEBUG = False
    PROD = True
    SECRET_KEY = environ.get('SECRET_KEY')
