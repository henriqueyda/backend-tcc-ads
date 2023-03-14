from marshmallow import fields

from ..models.user import User
from ..schemas import marshmallow


class UserSchema(marshmallow.Schema):
    class Meta:
        model = User

    id = fields.Integer()
    name = fields.String()
    email = fields.String()
    password = fields.String()
    address = fields.String()
    phone = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
