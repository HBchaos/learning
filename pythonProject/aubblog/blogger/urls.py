# blog/urls.py

from django.urls import path
from . import views
from .views import register_page

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("category/<category>/", views.blog_category, name="blog_category"),
    path("register/", register_page.as_view(), name="register_page"),

]