from django.db.models import QuerySet
from django.core.cache import cache
from config.settings import CACHE_ENABLED
from .models import Product


def get_products_of_category(category_id: int) -> QuerySet:
    """Функция возвращает список всех продуктов в указанной категории"""

    if CACHE_ENABLED:
        data = cache.get(f"products_of_{category_id}")
        if data is None:
            products = Product.objects.filter(category_id=category_id)
            cache.set(f"products_of_{category_id}", products, 30)
            return products

        return data

    return Product.objects.filter(category_id=category_id)
