import json

from django.conf import settings
from django.core.management import BaseCommand

from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser

def load_from_json(file_name):
    with open(f'{settings.BASE_DIR}/json/{file_name}.json', encoding='utf-8') as json_file:
        return json.load(json_file)



class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')
        ProductCategory.objects.all.delete()
        for cat in categories:
            ProductCategory.objects.create(**cat)
        products = load_from_json('products')
        Product.objects.all().delete()
        for prod in products:
            category_name = prod['category']
            _cat = ProductCategory.objects.get(name=category_name)
            prod['category'] = _cat
            ProductCategory.objects.create(**prod)
        super_user = ShopUser.objects.create_superuser('django',
                                                       'django@geekshop.local', 'geekbrains', age=33)

