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


class DevelopmentConfig(Config):
    """development application configurations"""
    DEBUG = True
    JWT_COOKIE_CSRF_PROTECT = False
    SQLALCHEMY_DATABASE_URL = 'sqlite:///db.sqlite3'
    ADMIN_TOKEN = 'sosecureijustcant'
    JWT_SECRET_KEY = 'topsecrettoken'


class TestingConfig(Config):
    """testing application configurations"""
    TESTING = True
