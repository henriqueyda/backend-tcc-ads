from datetime import datetime

from flask import Blueprint
from flask import current_app
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash

from app.models.user import User
from app.schemas.user import UserSchema

blueprint_user = Blueprint("user", __name__, url_prefix="/user")


@blueprint_user.route("/", methods=["POST"])
def create():
    user_schema = UserSchema()
    now = datetime.now().strftime("%Y-%m-%d")
    body = request.json
    body["password"] = generate_password_hash(body["password"], method="sha256")
    user = User(**request.json, created_at=now, updated_at=now)
    current_app.db.session.add(user)
    current_app.db.session.commit()
    return user_schema.jsonify(user), 201


@blueprint_user.route("/", methods=["GET"])
@jwt_required()
def get_all():
    user_schema = UserSchema(many=True)
    result = User.query.all()
    return user_schema.dump(result), 200


@blueprint_user.route("/<user_id>", methods=["GET"])
@jwt_required()
def get(user_id):
    user_schema = UserSchema()
    result = User.query.get_or_404(user_id)
    return user_schema.jsonify(result), 200


@blueprint_user.route("/current-user", methods=["GET"])
@jwt_required()
def get_current_user():
    user_schema = UserSchema()
    print(current_user.id)
    result = User.query.get_or_404(current_user.id)
    return user_schema.jsonify(result), 200


@blueprint_user.route("/<user_id>", methods=["PUT"])
@jwt_required()
def update(user_id):
    user_schema = UserSchema()
    now = datetime.now().strftime("%Y-%m-%d")
    result = User.query.filter(User.id == user_id)
    body = request.json
    body["updated_at"] = now
    result.update(body)
    current_app.db.session.commit()
    return user_schema.jsonify(result), 200


@blueprint_user.route("/<user_id>", methods=["DELETE"])
@jwt_required()
def delete(user_id):
    result = User.query.get_or_404(user_id)
    current_app.db.session.delete(result)
    current_app.db.session.commit()
    return "", 204
