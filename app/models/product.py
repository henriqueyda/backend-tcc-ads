from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from ..models import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    description = db.Column(db.String(255))
    color = db.Column(db.String(255))
    expiration_date = db.Column(db.Date)
    quantity = db.Column(db.Integer)
    picture = db.Column(URLType)
    price = db.Column(db.Numeric(10, 2))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = relationship("Category", back_populates="products")
    order_products = relationship("OrderProduct", back_populates="product")


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    products = relationship("Product", back_populates="category")
