from datetime import datetime
from functools import partial

from flask import Blueprint
from flask import current_app
from flask import request
from flask_jwt_extended import jwt_required

from ..models.model_factory import CategoryFactory
from ..models.model_factory import ProductFactory
from ..schemas.product import CategorySchema
from ..schemas.product import ProductSchema
from app.models.product import Category
from app.models.product import Product

blueprint_product = Blueprint("product", __name__, url_prefix="/product")


@blueprint_product.route("", methods=["GET"])
def index():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    filters = []
    category_name = request.args.get("category_name", type=str)
    if category_name:
        filters.append(partial(Product.category.has, name=category_name)())
    category_id = request.args.get("category_id", type=str)
    if category_id:
        filters.append(partial(Product.category_id.__eq__, category_id)())
    name = request.args.get("name", type=str)
    if name:
        filters.append(partial(Product.name.like, "Their purpose between.")())
    product_schema = ProductSchema(many=True)
    result = Product.query.filter(*filters).paginate(page=page, per_page=limit)
    iter_pages = [
        page_num
        for page_num in result.iter_pages(
            left_edge=1, right_edge=1, left_current=1, right_current=2
        )
    ]
    return {
        "total": result.total,
        "page": result.page,
        "limit": result.per_page,
        "iter_pages": iter_pages,
        "products": product_schema.dump(result.items),
    }, 200


@blueprint_product.route("/<product_id>", methods=["GET"])
@jwt_required()
def get_one(product_id):
    product_schema = ProductSchema()
    result = Product.query.get_or_404(product_id)
    return product_schema.jsonify(result), 200


@blueprint_product.route("/<product_id>", methods=["DELETE"])
@jwt_required()
def delete(product_id):
    result = Product.query.get_or_404(product_id)
    current_app.db.session.delete(result)
    current_app.db.session.commit()
    return "", 204


@blueprint_product.route("/<product_id>", methods=["PUT"])
@jwt_required()
def update(product_id):
    product_schema = ProductSchema()
    date = request.json.get("expiration_date")
    request.json["expiration_date"] = datetime.strptime(date, "%Y-%m-%d")
    result = Product.query.filter(Product.id == product_id)
    result.update(request.json)
    current_app.db.session.commit()
    return product_schema.jsonify(result.first_or_404()), 200


@blueprint_product.route("", methods=["POST"])
@jwt_required()
def create():
    product_schema = ProductSchema()
    date = request.json.get("expiration_date")
    request.json["expiration_date"] = datetime.strptime(date, "%Y-%m-%d")
    product = Product(**request.json)
    current_app.db.session.add(product)
    current_app.db.session.commit()
    return product_schema.jsonify(product), 201


@blueprint_product.route("/categories", methods=["GET"])
@jwt_required()
def index_category():
    category_schema = CategorySchema(many=True)
    result = Category.query.all()
    return category_schema.jsonify(result), 200


@blueprint_product.route("/populate/", methods=["GET"])
@jwt_required()
def populate():
    samples = request.args.get("samples", 30, type=int)
    current_app.db.drop_all()
    current_app.db.create_all()
    categories = [
        "Banheiros",
        "Cama, Mesa e Banho",
        "Climatização e Ventilação",
        "Decoração",
    ]

    for category in categories:
        category_factory = CategoryFactory.build(name=category)
        current_app.db.session.add(category_factory)
        current_app.db.session.commit()
        for product in ProductFactory.build_batch(int(samples / len(categories))):
            product.category = category_factory
            current_app.db.session.add(product)
            current_app.db.session.commit()

    return {"message": "Product table populated!"}, 200
