from flask import jsonify, request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.database import db_session as db
from db.models import Container

class CreateImage(Resource):
    """This endpoint grabs a token authentication is successful"""
    def get(self):
        """get request should return what this endpoint can do"""
        response = jsonify({"msg": "Post base_image and user_image"})
        return (response.json), 200


    @jwt_required
    def post(self):
        """A post request to this endpoint takes the base_image and
        user_image submitted via json and checks the database to ensure
        a match before issuing a token"""
        current_user = get_jwt_identity()
        print (current_user)
        if current_user is None:
                response = jsonify({"msg": "unauthenticated"})
                return (response.json), 401
        if not request.is_json:
            response = jsonify({"msg": "Missing JSON in request"})
            return (response.json), 400
        name = request.json.get('name', None)
        git_repo = request.json.get('git_repo', None)
        if not name:
            response = jsonify({"msg": "Missing name parameter"})
            return (response.json), 400 
        if not git_repo:
            response = jsonify({"msg": "Missing git_repo parameter"})
            return (response.json), 400
        query = User.query.filter_by(username=current_user).first()
        user_id = query.id
        print (user_id.int)
        db.add(Container(user_id, name, git_repo))
        db.commit()
        response = jsonify(status='building', name=name)
        return (response.json), 200


