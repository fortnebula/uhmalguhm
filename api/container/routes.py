from flask import jsonify, request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from dockerfile_parse import DockerfileParser

class BuildDocker(Resource):
    """This endpoint grabs a token authentication is successful"""
    def get(self):
        """get request should return what this endpoint can do"""
        response = jsonify({"msg": "Post username and password"})
        return (response.json), 200


    #@jwt_required
    def post(self):
        """A post request to this endpoint takes the username and
        password submitted via json and checks the database to ensure
        a match before issuing a token"""
        #current_user = get_jwt_identity()
        #response = jsonify(identity=current_user)
        dfp = DockerfileParser()
        dfp.content = request.get_data()
        #file = request.get_data()
        response = dfp.json
        return response, 200
