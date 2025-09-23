from django.contrib import admin

from catalog.models import Product, Category, Contacts


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "country",
        "individual_number",
        "address",
    )
    search_fields = (
        "country",
        "individual_number",
        "address",
    )
    list_filter = ("country",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = (
        "name",
        "description",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "category",
    )
    list_filter = ("category",)
    search_fields = (
        "name",
        "description",
    )
