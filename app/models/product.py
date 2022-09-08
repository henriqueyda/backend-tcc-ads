from ..models import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    description = db.Column(db.String(255))
    color = db.Column(db.String(255))
    expiration_date = db.Column(db.Date)
    quantity = db.Column(db.Integer)
