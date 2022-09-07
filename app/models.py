from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    app.db = db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    description = db.Column(db.String(255))
    color = db.Column(db.String(255))
    expiration_date = db.Column(db.Date)
    quantity = db.Column(db.Integer)
