from datetime import datetime
from flask import Blueprint, current_app, request

from app.models import Product
from ..serealizer import ProductSchema

blueprint_product = Blueprint("product", __name__, url_prefix="/product")


@blueprint_product.route("/", methods=["GET"])
def get_all():
    product_schema = ProductSchema(many=True)
    result = current_app.db.session.query(Product).all()
    return product_schema.jsonify(result), 200


@blueprint_product.route("/<product_id>", methods=["GET"])
def get_one(product_id):
    product_schema = ProductSchema()
    result = current_app.db.session.query(Product).filter_by(id=product_id).first()
    if result:
        return product_schema.jsonify(result), 200
    return "", 404


@blueprint_product.route("/<product_id>", methods=["DELETE"])
def delete(product_id):
    result = current_app.db.session.query(Product).filter_by(id=product_id).first()
    if result:
        current_app.db.session.delete(result)
        current_app.db.session.commit()
        return "", 204
    return "", 404


@blueprint_product.route("/<product_id>", methods=["PUT"])
def update(product_id):
    product_schema = ProductSchema()
    date = request.json.get("expiration_date")
    request.json["expiration_date"] = datetime.strptime(date, "%Y-%m-%d")
    result = current_app.db.session.query(Product).filter_by(id=product_id).first()
    if result:
        Product.query.filter(Product.id == product_id).update(request.json)
        current_app.db.session.commit()
        return product_schema.jsonify(result), 200
    return "", 404


@blueprint_product.route("/", methods=["POST"])
def create():
    product_schema = ProductSchema()
    date = request.json.get("expiration_date")
    request.json["expiration_date"] = datetime.strptime(date, "%Y-%m-%d")
    product = Product(**request.json)
    current_app.db.session.add(product)
    current_app.db.session.commit()
    return product_schema.jsonify(product), 201
