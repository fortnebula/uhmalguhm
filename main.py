"""This is the main application"""
# Package imports
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

# Local module imports
from umalguhm.config import DevelopmentConfig
from umalguhm.routes import Index, Token, Register
from umalguhm.db import init_db


# Main Application Initialization
app = Flask(__name__)
app.config.from_object(DevelopmentConfig())
api = Api(app)
jwt = JWTManager(app)

# API endpoints for this application
api.add_resource(Index, '/')
api.add_resource(Token, '/token')
api.add_resource(Register, '/register')

if __name__ == '__main__':
    init_db()
    app.run()
