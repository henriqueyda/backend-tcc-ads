from datetime import datetime

import sqlalchemy as sa
from flask import Blueprint
from flask import current_app
from flask import request

from ..models.model_factory import ProductFactory
from ..schemas.product import ProductSchema
from app.models.product import Product

blueprint_product = Blueprint("product", __name__, url_prefix="/product")


@blueprint_product.route("/", methods=["GET"])
def index():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    product_schema = ProductSchema(many=True)
    result = Product.query.paginate(page=page, per_page=limit)
    return {
        "total": result.total,
        "page": result.page,
        "limit": result.per_page,
        "count": len(result.items),
        "products": product_schema.dump(result.items),
    }, 200


@blueprint_product.route("/<product_id>", methods=["GET"])
def get_one(product_id):
    product_schema = ProductSchema()
    result = Product.query.get_or_404(product_id)
    return product_schema.jsonify(result), 200


@blueprint_product.route("/<product_id>", methods=["DELETE"])
def delete(product_id):
    result = Product.query.get_or_404(product_id)
    current_app.db.session.delete(result)
    current_app.db.session.commit()
    return "", 204


@blueprint_product.route("/<product_id>", methods=["PUT"])
def update(product_id):
    product_schema = ProductSchema()
    date = request.json.get("expiration_date")
    request.json["expiration_date"] = datetime.strptime(date, "%Y-%m-%d")
    result = Product.query.filter(Product.id == product_id)
    result.update(request.json)
    current_app.db.session.commit()
    return product_schema.jsonify(result.first_or_404()), 200


@blueprint_product.route("/", methods=["POST"])
def create():
    product_schema = ProductSchema()
    date = request.json.get("expiration_date")
    request.json["expiration_date"] = datetime.strptime(date, "%Y-%m-%d")
    product = Product(**request.json)
    current_app.db.session.add(product)
    current_app.db.session.commit()
    return product_schema.jsonify(product), 201


@blueprint_product.route("/populate/", methods=["GET"])
def populate():
    inspector = sa.inspect(current_app.db.engine)
    if inspector.has_table("product"):
        Product.__table__.drop(current_app.db.engine)
    Product.__table__.create(current_app.db.engine)
    for product in ProductFactory.build_batch(30):
        current_app.db.session.add(product)
        current_app.db.session.commit()
    return {"message": "Product table populated!"}, 200
