from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("users/", views.user_accounts, name="user_accounts"),
    path("admins/", views.admin_accounts, name="admin_accounts"),
    path("delete/<str:cust_email>/", views.delete_customer, name="delete_customer"),
    # path("delete/<str:admin_email>/", views.delete_admin, name="delete_admin"),
]
