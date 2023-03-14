import enum

from sqlalchemy import Enum
from sqlalchemy.orm import relationship

from ..models import db


class Status(enum.Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = relationship("User", back_populates="orders")
    order_products = relationship("OrderProduct", back_populates="order")
    total_price = db.Column(db.Numeric(10, 2))
    delivery_address = db.Column(db.String(255))
    delivery_city = db.Column(db.String(255))
    delivery_state = db.Column(db.String(255))
    delivery_zip = db.Column(db.String(255))
    delivery_reference = db.Column(db.String(255))
    status = db.Column(Enum(Status))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)


class OrderProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    order = relationship("Order", back_populates="order_products")
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    product = relationship("Product", back_populates="order_products")
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
