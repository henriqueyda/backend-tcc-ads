import os

import stripe
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from .models import configure as config_db
from .models.user import User
from .schemas import configure as config_ma
from config import Config


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    config_db(app)
    config_ma(app)
    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(email=identity).one_or_none()

    Migrate(app, app.db, compare_type=True)
    stripe_keys = {
        "secret_key": os.environ["STRIPE_SECRET_KEY"],
        "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
    }

    stripe.api_key = stripe_keys["secret_key"]
    app.stripe = stripe

    from .routes.product import blueprint_product
    from .routes.shopping_cart import blueprint_shopping_cart
    from .routes.order import blueprint_order
    from .routes.user import blueprint_user
    from .routes.auth import blueprint_auth

    app.register_blueprint(blueprint_product)
    app.register_blueprint(blueprint_shopping_cart)
    app.register_blueprint(blueprint_order)
    app.register_blueprint(blueprint_user)
    app.register_blueprint(blueprint_auth)

    return app
