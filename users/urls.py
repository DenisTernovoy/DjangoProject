from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from .apps import UsersConfig
from .views import confirm_email

app_name = UsersConfig.name

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("<int:pk>/update/", views.UserUpdateView.as_view(), name="update"),
    path("confirm-email/<str:token>/", confirm_email, name="confirm_email"),
]
