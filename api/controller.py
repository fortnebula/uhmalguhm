from flask import Flask
from flask_restx import Api
from api.auth.routes import (Version, IssueTokens, RefreshTokens, UserCreate)
from api.container.routes import CreateImage


def register_routes(app: Flask) -> None: # noqa
    api = Api(app) # noqa
    api.add_resource(Version, '/api/v1/')
    api.add_resource(IssueTokens, '/api/v1/token/issue')
    api.add_resource(RefreshTokens, '/api/v1/token/refresh')
    api.add_resource(UserCreate, '/api/v1/user/create')
    api.add_resource(CreateImage, '/api/v1/container/create')
