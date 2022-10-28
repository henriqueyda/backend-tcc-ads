import factory
import requests
from faker import Faker

from app.models.product import Category
from app.models.product import Product


faker = Faker()


def generate_random_pics():
    return requests.get("https://picsum.photos/500").url


class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Category

    description = factory.Faker("sentence", nb_words=30, variable_nb_words=False)


class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("sentence", nb_words=3, variable_nb_words=False)
    brand = factory.Faker("company")
    description = factory.Faker("sentence", nb_words=30, variable_nb_words=False)
    color = factory.Faker("color_name")
    expiration_date = factory.Faker("date_between", start_date="today", end_date="+10y")
    quantity = factory.Faker("random_int")
    picture = "https://cec-a.akamaihd.net/img-prod/images/standard/cimento-todas-as-obras-50kg-votorantim-1228972-foto-a644e307-1919-4c4b-8737-b62144cc1932.png"
    price = factory.Faker("pyfloat", left_digits=4, right_digits=2, positive=True)
