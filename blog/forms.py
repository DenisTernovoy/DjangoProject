from django import forms

from blog.models import BlogNote
from config.forms import StyleFormMixin


class BlogNoteForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = BlogNote
        exclude = [
            "created_at",
            "views_counter",
            "owner",
        ]
