from django.contrib import admin
from .models import BlogNote

# Register your models here.


@admin.register(BlogNote)
class BlogNoteAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "preview", "created_at")
    search_fields = ("title", "content")
