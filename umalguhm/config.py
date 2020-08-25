"""This module provides the application configurations"""
from os import urandom


class Config():
    """Main application configurations"""
    DEBUG = False
    TESTING = False
    JWT_TOKEN_LOCATION = 'headers'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_SECRET_KEY = urandom(32)


class ProductionConfig(Config):
    """production application configurations"""
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    """development application configurations"""
    DEBUG = True
    JWT_COOKIE_CSRF_PROTECT = False


class TestingConfig(Config):
    """testing application configurations"""
    TESTING = True
