import datetime

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from app.models.user import User

blueprint_auth = Blueprint("auth", __name__, url_prefix="/auth")


@blueprint_auth.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if username and password:
        user = User.query.filter_by(email=username).first()
        if user and check_password_hash(user.password, password):
            token = create_access_token(
                identity=username,
                expires_delta=datetime.timedelta(minutes=30),
                additional_claims={"is_admin": user.is_admin},
            )

            return jsonify({"token": token})
        return make_response(
            "Incorrect user or password",
            401,
            {"WWW-Authenticate": 'Basic realm="Login Required"'},
        )

    return make_response(
        "Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )
