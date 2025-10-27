from .apps import BlogConfig
from django.urls import path
from . import views

app_name = BlogConfig.name

urlpatterns = [
    path("", views.BlogListView.as_view(), name="blog_list"),
    path("add_note/", views.BlogCreateView.as_view(), name="blog_create"),
    path("<int:pk>/", views.BlogDetailView.as_view(), name="blog_detail"),
    path("<int:pk>/edit/", views.BlogUpdateView.as_view(), name="blog_update"),
    path("<int:pk>/delete/", views.BlogDeleteView.as_view(), name="blog_delete"),
    path("<int:pk>/drop/", views.drop_blog_note, name="blog_drop"),
    path("<int:pk>/public/", views.public_blog_note, name="blog_public"),
    path("users/<int:pk>/blog/", views.UserBlogListView.as_view(), name="my_blog"),
]
