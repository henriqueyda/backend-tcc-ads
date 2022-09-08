from ..models.product import Product
from ..schemas import marshmallow


class ProductSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
