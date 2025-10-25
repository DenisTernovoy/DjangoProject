from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True, verbose_name="Аватар"
    )
    phone = models.CharField(
        max_length=15, null=True, blank=True, verbose_name="Мобильный телефон"
    )
    country = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Страна"
    )
    token = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Токен авторизации"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
