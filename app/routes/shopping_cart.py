from datetime import datetime

import redis
from flask import Blueprint
from flask import current_app
from flask import request
from redis.commands.json.path import Path

from app.models.product import Product

blueprint_shopping_cart = Blueprint(
    "shopping_cart", __name__, url_prefix="/shopping_cart"
)


@blueprint_shopping_cart.route("/add", methods=["POST"])
def add():
    r: redis.client.Redis = current_app.redis
    body = request.json

    result = Product.query.get_or_404(body["product_id"])

    with r.pipeline() as pipe:
        if not r.exists(body["user_id"]):
            pipe.json().set(
                body["user_id"],
                Path.root_path(),
                {
                    "total_price": 0,
                    "items": {},
                    "created_at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                    "updated_at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                },
            )
        products_ids = r.json().objkeys(body["user_id"], Path(".items"))
        if not products_ids or str(body["product_id"]) not in products_ids:
            pipe.json().set(
                body["user_id"],
                Path(f".items.{body['product_id']}"),
                {
                    "quantity": 0,
                    "price": float(result.price),
                    "created_at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                    "updated_at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                },
            )
        pipe.json().numincrby(
            body["user_id"],
            Path(f".items.{body['product_id']}.quantity"),
            body["quantity"],
        )
        pipe.json().numincrby(
            body["user_id"],
            Path(".total_price"),
            float(result.price * body["quantity"]),
        )
        pipe.json().set(
            body["user_id"],
            Path(".updated_at"),
            datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        )
        pipe.json().set(
            body["user_id"],
            Path(f".items.{body['product_id']}.updated_at"),
            datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        )
        pipe.execute()
    return r.json().get(body["user_id"])
