from os import urandom

class Config(object):
    DEBUG = False
    TESTING = False
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_ACCESS_COOKIE_PATH = '/api/'
    JWT_REFRESH_COOKIE_PATH = '/token/refresh'
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_SECRET_KEY = urandom(32)

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_SECRET_KEY = 'super-secret'

class TestingConfig(Config):
    TESTING = True