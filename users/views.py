import secrets

from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from config import settings
from .forms import CustomUserCreationForm
from .models import CustomUser


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email
        token = secrets.token_hex(16)
        user.token = token
        user.is_active = False
        user.save()
        host = self.request.get_host()

        url = f"http://{host}/users/confirm-email/{token}"

        self.send_welcome_email(user.email, url)

        return super().form_valid(form)

    @staticmethod
    def send_welcome_email(user_email, confirm_url):
        subject = "Регистрация в E-Shop"
        message = f"Подтвердите регистрацию в магазине E-Shop. Для этого перейдите по ссылке {confirm_url}"
        from_email = settings.EMAIL_HOST_USER

        recipient_list = [
            user_email,
        ]
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
        )


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("catalog:product_list")


def confirm_email(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()

    return redirect("users:login")
