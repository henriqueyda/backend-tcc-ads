import redis
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    app.db = db
    redis.Redis()
    app.redis = redis.Redis()
