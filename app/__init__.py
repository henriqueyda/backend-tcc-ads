from flask import Flask
from config import Config
from flask_migrate import Migrate
from .models import configure as config_db
from .serealizer import configure as config_ma


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    config_db(app)
    config_ma(app)

    Migrate(app, app.db)

    from .routes.product import blueprint_product

    app.register_blueprint(blueprint_product)

    return app
