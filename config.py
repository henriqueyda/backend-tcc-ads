class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql://local_user:admin123@localhost/casa_leite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "my_secret_key"
