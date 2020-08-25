# Package imports

from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

# Local module imports
from .db import db_session
from .models import PassGen, User

class Index(Resource):
    def get(self):
        response = jsonify({"version": "v0.0.1"})
        return (response.json), 200

# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
class Token(Resource):
    def get(self):
        response = jsonify({"msg": "Post username and password"})
        return (response.json), 200

    def post(self):
        if not request.is_json:
            response = jsonify({"msg": "Missing JSON in request"})
            return (response.json), 400
    
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username:
            response = jsonify({"msg": "Missing username parameter"})
            return (response.json), 400
        if not password:
            response = jsonify({"msg": "Missing password parameter"})
            return (response.json), 400    
        query = User.query.filter_by(username=username).first()
        verifypass = PassGen.decryptpass(password, query.password)
        if verifypass == True:     
            # Identity can be any data that is json serializable
            access_token = create_access_token(identity=username)
            response = jsonify(access_token=access_token)
            return (response.json), 200
        response = jsonify({"msg": "unauthenticated"})
        return (response.json), 401

class Register(Resource):
    def get(self):
        data = {
        'error': 'this endpoint does not accept get requests, try posting with curl'
        }
        return data

    def post(self):
        if not request.is_json:
            response = jsonify({"msg": "Missing JSON in request"})
            return (response.json), 400
    
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username:
            response = jsonify({"msg": "Missing username parameter"})
            return (response.json), 400
        if not password:
            response = jsonify({"msg": "Missing password parameter"})
            return (response.json), 400
        crypt_pass = PassGen.cryptpass(password)
        adduser = db_session.add(User(username, crypt_pass))
        db_session.commit()
        response = jsonify(status='registered', username=username) 
        return (response.json), 200
# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
#@app.route('/protected', methods=['GET'])
#@jwt_required
#def protected():
    # Access the identity of the current user with get_jwt_identity
#    current_user = get_jwt_identity()
#    return jsonify(logged_in_as=current_user), 200
