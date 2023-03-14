from marshmallow import fields

from ..models.order import Order
from ..models.order import OrderProduct
from ..schemas import marshmallow


class OrderSchema(marshmallow.Schema):
    class Meta:
        model = Order

    id = fields.Integer()
    user_id = fields.Integer()
    order_products = fields.Nested("OrderProductSchema", many=True)
    total_price = fields.Float()
    delivery_address = fields.String()
    delivery_city = fields.String()
    delivery_state = fields.String()
    delivery_zip = fields.String()
    delivery_reference = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class OrderProductSchema(marshmallow.Schema):
    class Meta:
        model = OrderProduct

    order_id = fields.Integer()
    product_id = fields.Integer()
    product = fields.Nested("ProductSchema")
    quantity = fields.Integer()
    price = fields.Float()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
