from flask_marshmallow import Marshmallow

marshmallow = Marshmallow()


def configure(app):
    marshmallow.init_app(app)
