from django.urls import path
from . import views
from .apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("contacts/", views.ContactsView.as_view(), name="contacts_view"),
    path(
        "product_detail/<int:pk>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
    path("add_product/", views.ProductCreateView.as_view(), name="product_create"),
    path(
        "product_detail/<int:pk>/update/",
        views.ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "product_detail/<int:pk>/delete/",
        views.ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path(
        "categories/",
        views.CategoryListView.as_view(),
        name="categories_list",
    ),
    path(
        "categories/<int:pk>/>",
        views.ProductsCategoryListView.as_view(),
        name="products_category",
    ),
]
