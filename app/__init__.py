from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from .models import configure as config_db
from .schemas import configure as config_ma
from config import Config


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    config_db(app)
    config_ma(app)

    Migrate(app, app.db, compare_type=True)

    from .routes.product import blueprint_product
    from .routes.shopping_cart import blueprint_shopping_cart

    app.register_blueprint(blueprint_product)
    app.register_blueprint(blueprint_shopping_cart)

    return app
