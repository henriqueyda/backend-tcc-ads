from datetime import datetime

from flask import Blueprint
from flask import current_app
from flask import request

from app.models.user import User
from app.schemas.user import UserSchema

blueprint_user = Blueprint("user", __name__, url_prefix="/user")


@blueprint_user.route("/", methods=["POST"])
def create():
    user_schema = UserSchema()
    now = datetime.now().strftime("%Y-%m-%d")
    user = User(**request.json, created_at=now, updated_at=now)
    current_app.db.session.add(user)
    current_app.db.session.commit()
    return user_schema.jsonify(user), 201
