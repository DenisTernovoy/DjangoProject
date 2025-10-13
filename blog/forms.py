from django import forms

from blog.models import BlogNote


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            print(field)
            if isinstance(field, forms.BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class BlogNoteForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = BlogNote
        exclude = ["created_at", "views_counter"]
