from typing import Any
from django import forms

from core.models import Rating, Restaurant, Order


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ("restaurant", "user", "rating")


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ("name", "restaurant_type")


class ProductStockException(Exception):
    pass


class ProductOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("product", "number_of_items")

    def save(self, commit: bool = True) -> Any:
        order: Order = super().save(commit=False)
        if order.product.number_in_stock < order.number_of_items:
            raise ProductStockException(
                f"Not enough items in stocks for product: {order.product}"
            )

        if commit:
            order.save()
        return order
