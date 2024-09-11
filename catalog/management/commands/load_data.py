import json
from django.core.management import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open('catalog/fixture/catalog_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            categories = []
            for item in data:
                if item['model'] == 'catalog.category':
                    categories.append(item)
            return categories


    @staticmethod
    def json_read_products():
        with open('catalog/fixture/catalog_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            products = []
            for item in data:
                if item['model'] == 'catalog.product':
                    products.append(item)
            return products

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        categories_for_create = []
        for category in Command.json_read_categories():
            category_data = category["fields"]
            categories_for_create.append(Category(id=category["pk"], **category_data))
        Category.objects.bulk_create(categories_for_create)

        products_for_create = []
        for product in Command.json_read_products():
            product_data = product["fields"]
            category = Category.objects.get(pk=product_data.pop("category"))
            products_for_create.append(
                Product(id=product["pk"], category=category, **product_data)
            )
        Product.objects.bulk_create(products_for_create)
