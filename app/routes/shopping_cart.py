from datetime import datetime

import redis
from flask import Blueprint
from flask import current_app
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from redis.commands.json.path import Path

from app.models.product import Product

blueprint_shopping_cart = Blueprint(
    "shopping_cart", __name__, url_prefix="/shopping_cart"
)


@blueprint_shopping_cart.route("", methods=["GET"])
@jwt_required()
def get_one():
    r: redis.client.Redis = current_app.redis
    shopping_cart = r.json().get(current_user.id)
    if shopping_cart:
        return r.json().get(current_user.id)
    return {"message": "Shopping cart not found"}, 404


@blueprint_shopping_cart.route("/add", methods=["POST"])
@jwt_required()
def add():
    r: redis.client.Redis = current_app.redis
    body = request.json

    result = Product.query.get_or_404(body["product_id"])
    if result.quantity - body["quantity"] < 0:
        return {"message": "Out of stock"}, 200

    with r.pipeline() as pipe:
        if not r.exists(current_user.id):
            pipe.json().set(
                current_user.id,
                Path.root_path(),
                {
                    "total_price": 0,
                    "items": {},
                    "created_at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                    "updated_at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                },
            )
        products_ids = r.json().objkeys(current_user.id, Path(".items"))
        if not products_ids or str(body["product_id"]) not in products_ids:
            pipe.json().set(
                current_user.id,
                Path(f".items.{body['product_id']}"),
                {
                    "quantity": 0,
                    "price": float(result.price),
                    "name": result.name,
                    "description": result.description,
                    "picture": result.picture,
                    "created_at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                    "updated_at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                },
            )

        pipe.json().set(
            current_user.id,
            Path(f".items.{body['product_id']}.price"),
            float(result.price),
        )
        pipe.json().set(
            current_user.id,
            Path(f".items.{body['product_id']}.name"),
            result.name,
        )
        pipe.json().set(
            current_user.id,
            Path(f".items.{body['product_id']}.description"),
            result.description,
        )

        pipe.json().numincrby(
            current_user.id,
            Path(f".items.{body['product_id']}.quantity"),
            body["quantity"],
        )
        pipe.json().numincrby(
            current_user.id,
            Path(".total_price"),
            float(result.price * body["quantity"]),
        )
        pipe.json().set(
            current_user.id,
            Path(".updated_at"),
            datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        )
        pipe.json().set(
            current_user.id,
            Path(f".items.{body['product_id']}.updated_at"),
            datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        )
        pipe.execute()

    Product.query.filter(Product.id == body["product_id"]).update(
        {"quantity": result.quantity - body["quantity"]}
    )
    current_app.db.session.commit()

    return r.json().get(current_user.id)


@blueprint_shopping_cart.route("/remove", methods=["POST"])
@jwt_required()
def remove():
    r: redis.client.Redis = current_app.redis
    body = request.json

    result = Product.query.get_or_404(body["product_id"])

    with r.pipeline() as pipe:
        if not r.exists(current_user.id):
            return {"message": "Shopping cart not found"}, 404

        products_ids = r.json().objkeys(current_user.id, Path(".items"))
        if str(body["product_id"]) not in products_ids:
            return {"message": "Product not found"}, 404

        cart_quantity = r.json().get(
            current_user.id, Path(f".items.{body['product_id']}.quantity")
        )
        pipe.json().numincrby(
            current_user.id,
            Path(".total_price"),
            float(-1 * result.price * body["quantity"]),
        )
        pipe.json().delete(current_user.id, Path(f".items.{body['product_id']}"))
        pipe.execute()

    Product.query.filter(Product.id == body["product_id"]).update(
        {"quantity": result.quantity + int(cart_quantity)}
    )
    current_app.db.session.commit()

    return r.json().get(current_user.id)


@blueprint_shopping_cart.route("/", methods=["DELETE"])
@jwt_required()
def delete():
    r: redis.client.Redis = current_app.redis
    shopping_cart = r.json().get(current_user.id)
    if shopping_cart:
        r.delete(current_user.id)
        return {"message": "Shopping cart deleted"}, 200
    return {"message": "Shopping cart not found"}, 404
