from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Створює кілька демо-категорій і товарів для перевірки магазину'

    def handle(self, *args, **options):
        data = {
            'Свічки': [
                ('Свічка лавандова', 320),
                ('Свічка соєва "Кориця"', 280),
            ],
            'Кераміка': [
                ('Чашка ручної роботи', 450),
                ('Тарілка декоративна', 600),
            ],
            'Текстиль': [
                ('Плед бавовняний', 1200),
                ('Подушка декоративна', 540),
            ],
        }

        for category_name, products in data.items():
            category, _ = Category.objects.get_or_create(name=category_name)
            for product_name, price in products:
                Product.objects.get_or_create(
                    name=product_name,
                    category=category,
                    defaults={'price': price, 'description': 'Опис товару скоро з’явиться.'},
                )

        self.stdout.write(self.style.SUCCESS('Демо-товари створено! Зайди на сайт і подивись.'))
