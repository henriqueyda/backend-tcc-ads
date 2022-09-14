from datetime import datetime

from flask import Blueprint
from flask import current_app
from flask import request

from ..schemas.product import ProductSchema
from app.models.product import Product

blueprint_product = Blueprint("product", __name__, url_prefix="/product")


@blueprint_product.route("/", methods=["GET"])
def get_all():
    product_schema = ProductSchema(many=True)
    result = Product.query.all()
    return product_schema.jsonify(result), 200


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
    request.json["expiration_date"] = datetime.strptime(date, "%d/%m/%Y")
    result = Product.query.filter(Product.id == product_id)
    result.update(request.json)
    current_app.db.session.commit()
    return product_schema.jsonify(result.first_or_404()), 200


@blueprint_product.route("/", methods=["POST"])
def create():
    product_schema = ProductSchema()
    date = request.json.get("expiration_date")
    request.json["expiration_date"] = datetime.strptime(date, "%d/%m/%Y")
    product = Product(**request.json)
    current_app.db.session.add(product)
    current_app.db.session.commit()
    return product_schema.jsonify(product), 201
