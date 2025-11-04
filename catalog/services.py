from django.db.models import QuerySet

from .models import Product


def get_products_of_category(category_id: int) -> QuerySet:
    """Функция возвращает список всех продуктов в указанной категории"""

    products = Product.objects.filter(category_id=category_id)

    return products
