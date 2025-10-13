from django import forms
from catalog.models import Product
from django.forms import ValidationError


class ProductForm(forms.ModelForm):

    EXCLUDE_WORDS = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    class Meta:
        model = Product
        fields = ["name", "description", "price", "category", "image"]

    def clean_name(self):
        cleaned_data = super().clean()

        name = cleaned_data.get("name")

        for word in name.split():
            if word.lower() in self.EXCLUDE_WORDS:
                raise ValidationError(
                    f"Поле 'Наименование' не может содержать слово {word}"
                )

        if Product.objects.filter(name=name).exists():
            raise ValidationError("Продукт с таким наименованием уже существует")

        return name

    def clean_description(self):
        cleaned_data = super().clean()

        description = cleaned_data.get("description")

        for word in description.split():
            if word.lower() in self.EXCLUDE_WORDS:
                raise ValidationError(
                    f"Поле 'Описание' не может содержать слово {word}"
                )

        return description
