from django.db import models

from users.models import CustomUser


# Create your models here.


class BlogNote(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    preview = models.ImageField(upload_to="blog/photo", verbose_name="Изображение")

    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Автор"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=True, verbose_name="Метка публикации")
    views_counter = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ["-created_at"]
        permissions = [
            ("can_unpublish_blog_note", "Can unpublish Blog note"),
        ]
