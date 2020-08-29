from celery import Celery
from db.database import init_db
from flask_jwt_extended import JWTManager


celery = Celery()


def register_extensions(app, worker=False):
    jwt = JWTManager(app) # noqa
    init_db(app)
    # load celery config
    celery.config_from_object(app.config)

    if not worker:
        # register celery irrelevant extensions
        pass
