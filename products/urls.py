from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("users/", views.user_index, name="user_index"),
    path("add-products/", views.add_products, name="add_products"),
    path("download/csv/", views.download_csv, name="download_csv"),
    path("download/excel/", views.download_excel, name="download_excel"),
    path("delete/<str:product_name>/", views.delete_product, name="delete_product"),
    path("edit/<str:product_name>/", views.edit_product, name="edit_product"),
    path("update/<str:product_name>/", views.update_product, name="update_product"),
    path("download/user/csv/", views.user_download_csv, name="user_download_csv"),
    path("download/user/excel/", views.user_download_excel, name="user_download_excel"),
]
