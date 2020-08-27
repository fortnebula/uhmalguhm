"""This is the main application"""
# Package imports
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api

# Local module imports
from conf.config import DevelopmentConfig
from api.auth.routes import (Version, IssueTokens,
                             RefreshTokens, UserCreate)
from api.container.routes import BuildDocker
from db.database import init_db


# Main Application Initialization
app = Flask(__name__)
app.config.from_object(DevelopmentConfig())
api = Api(app)
jwt = JWTManager(app)

# API endpoints for this application
api.add_resource(Version, '/api/v1/')
api.add_resource(IssueTokens, '/api/v1/token/issue')
api.add_resource(RefreshTokens, '/api/v1/token/refresh')
api.add_resource(UserCreate, '/api/v1/user/create')
api.add_resource(BuildDocker, '/api/v1/container/build')


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run()
