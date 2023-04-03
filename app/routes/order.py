from datetime import datetime

from flask import Blueprint
from flask import current_app
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required

from app.models.order import Order
from app.models.order import OrderProduct
from app.models.product import Product
from app.schemas.order import OrderProductSchema
from app.schemas.order import OrderSchema

blueprint_order = Blueprint("order", __name__, url_prefix="/order")


@blueprint_order.route("", methods=["GET"])
@jwt_required()
def get_user_orders():
    order_schema = OrderSchema(many=True)
    result = Order.query.filter_by(user_id=current_user.id).all()
    return order_schema.dump(result), 200


@blueprint_order.route("/", methods=["GET"])
@jwt_required()
def get_all_orders():
    order_schema = OrderSchema(many=True)
    result = Order.query.all()
    return order_schema.dump(result), 200


@blueprint_order.route("/<order_id>", methods=["DELETE"])
@jwt_required()
def delete(order_id):
    result = Order.query.get_or_404(order_id)
    current_app.db.session.delete(result)
    current_app.db.session.commit()
    return "", 204


@blueprint_order.route("/", methods=["POST"])
@jwt_required()
def create():
    total_price = request.json.get("total_price", None)
    delivery_address = request.json.get("delivery_address", None)
    delivery_city = request.json.get("delivery_city", None)
    delivery_state = request.json.get("delivery_state", None)
    delivery_zip = request.json.get("delivery_zip", None)
    delivery_reference = request.json.get("delivery_reference", None)
    status = request.json.get("status", None)
    now = datetime.now().strftime("%Y-%m-%d")
    order_schema = OrderSchema()
    order = Order(
        user_id=current_user.id,
        total_price=total_price,
        delivery_address=delivery_address,
        delivery_city=delivery_city,
        delivery_state=delivery_state,
        delivery_zip=delivery_zip,
        delivery_reference=delivery_reference,
        status=status,
        created_at=now,
        updated_at=now,
    )
    current_app.db.session.add(order)
    current_app.db.session.commit()
    return order_schema.jsonify(order), 201


@blueprint_order.route("/<order_id>/product/<product_id>", methods=["POST"])
@jwt_required()
def add_order_product(order_id, product_id):
    Order.query.get_or_404(order_id)

    now = datetime.now().strftime("%Y-%m-%d")
    quantity = request.json.get("quantity", None)
    Product.query.get_or_404(product_id)
    order_product = OrderProduct(
        order_id=order_id,
        product_id=product_id,
        created_at=now,
        updated_at=now,
        quantity=quantity,
    )
    current_app.db.session.add(order_product)
    current_app.db.session.commit()
    return "", 204


@blueprint_order.route("/<order_id>/product", methods=["GET"])
@jwt_required()
def get_order_product(order_id):
    order_schema = OrderProductSchema(many=True)
    result = OrderProduct.query.filter_by(order_id=order_id)
    return order_schema.dump(result), 200


@blueprint_order.route("/<order_id>/product/<product_id>", methods=["DELETE"])
@jwt_required()
def delete_order_product(order_id, product_id):
    result = OrderProduct.query.filter_by(
        order_id=order_id, product_id=product_id
    ).first_or_404()
    current_app.db.session.delete(result)
    current_app.db.session.commit()
    return "", 204
