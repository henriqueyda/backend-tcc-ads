from flask_marshmallow import Marshmallow
from marshmallow import fields
from .models import Product

marshmallow = Marshmallow()


def configure(app):
    marshmallow.init_app(app)


class ProductSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
