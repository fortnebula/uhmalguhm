from flask import jsonify, request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.database import db_session as db
from db.models import User, Container
from api.container import tasks


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
        if current_user is None:
            response = jsonify({"msg": "unauthenticated"})
            return (response.json), 401
        if not request.is_json:
            response = jsonify({"msg": "Missing JSON in request"})
            return (response.json), 400
        docker_image = request.json.get('image', None)
        docker_tag = request.json.get('tag', None)
        if not docker_image:
            response = jsonify({"msg": "Missing docker image parameter"})
            return (response.json), 400
        if not docker_tag:
            response = jsonify({"msg": "Missing docker tag parameter"})
            return (response.json), 400
        query = User.query.filter_by(username=current_user).first()
        user_id = query.uuid
        status = 'building'
        container_id = Container(user_id, docker_image, docker_tag, status)
        db.add(container_id)
        db.commit()
        tasks.create_image.apply_async(args=[container_id.uuid,
                                       docker_image, docker_tag])
        response = jsonify(status=status, id=container_id.uuid)
        return (response.json), 200
