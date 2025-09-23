import json
from itertools import product
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = "Load test data categories and products from catalog_fixture"

    def handle(self, *args, **kwargs):
        Category.objects.all().delete()
        Product.objects.all().delete()

        call_command("loaddata", "catalog_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))

        products = [
            {
                "name": "iPhone 16",
                "description": "Отличный телефон",
                "category_id": 1,
                "price": 65000.00,
            },
            {
                "name": "Nokia A2310",
                "description": "Лучший телефон",
                "category_id": 1,
                "price": 1000.00,
            },
            {
                "name": "Motorola W",
                "description": "Легендарный телефон",
                "category_id": 1,
                "price": 800.00,
            },
        ]

        for item in products:
            new_product, created = Product.objects.get_or_create(**item)
            new_product.save()

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created product {new_product.name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Product {new_product.name} already exists")
                )
