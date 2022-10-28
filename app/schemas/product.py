from marshmallow import fields

from ..models.product import Category
from ..models.product import Product
from ..schemas import marshmallow


class ProductSchema(marshmallow.Schema):
    class Meta:
        model = Product

    id = fields.Integer()
    name = fields.String()
    brand = fields.String()
    description = fields.String()
    color = fields.String()
    expiration_date = fields.Date(format="%d/%m/%Y")
    quantity = fields.Integer()
    picture = fields.URL()
    price = fields.Float()
    category_id = fields.Integer()


class CategorySchema(marshmallow.Schema):
    class Meta:
        model = Category

    id = fields.Integer()
    name = fields.String()
    brand = fields.String()
    description = fields.String()
