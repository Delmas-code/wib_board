from django.urls import path
from . import views

app_name = "base"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("create/", views.create_admin, name="create_admin"),
]
