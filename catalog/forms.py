from django import forms
from catalog.models import Product
from django.forms import ValidationError


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.instance_data = kwargs.get("instance")

        for field_name, field in self.fields.items():
            if isinstance(field, forms.CheckboxInput):
                field.widget.attrs.update(
                    {
                        "class": "form-check",
                    }
                )
            else:
                field.widget.attrs.update(
                    {
                        "class": "form-control",
                    }
                )


class ProductForm(StyleFormMixin, forms.ModelForm):

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
        name = self.cleaned_data.get("name")

        for word in name.split():
            if word.lower() in self.EXCLUDE_WORDS:
                raise ValidationError(
                    f"Поле 'Наименование' не может содержать слово {word}"
                )

        if Product.objects.filter(name=name).exists():
            if self.instance_data is not None:
                name_base = self.instance_data.name
                if name_base != name:
                    raise ValidationError(
                        "Продукт с таким наименованием уже существует"
                    )
            else:
                raise ValidationError("Продукт с таким наименованием уже существует")

        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")

        for word in description.split():
            if word.lower() in self.EXCLUDE_WORDS:
                raise ValidationError(
                    f"Поле 'Описание' не может содержать слово {word}"
                )

        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")

        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")

        return price

    def clean_image(self):
        file = self.cleaned_data.get("image")

        if file:
            valid_extensions = [".jpeg", ".png"]
            if not file.name.endswith(tuple(valid_extensions)):
                raise forms.ValidationError(
                    "Недопустимый тип файла. Допустимые типы: JPEG или PNG."
                )

            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Размер файла не должен превышать 5 МБ.")

        return file
