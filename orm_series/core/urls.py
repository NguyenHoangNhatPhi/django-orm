from django.urls import path

from core import views

urlpatterns = [
    path("", views.index, name="index"),
    path("restaurant/", views.restaurant, name="restaurant"),
    path("order/", views.order_product, name="order-product"),
]
