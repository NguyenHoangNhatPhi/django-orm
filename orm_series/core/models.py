from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):

    class TypeChoices(models.TextChoices):
        ITALIAN = "IT", "Italian"
        INDIAN = "IN", "Indian"
        CHINESE = "CH", "Chinese"
        GREEK = "GR", "Greek"
        MEXICAN = "MX", "Mexican"
        FASTFOOD = "FF", "Fast Food"
        OTHER = "OT", "Other"

    name = models.CharField(max_length=100)
    website = models.URLField(default="")
    date_opened = models.DateField()
    latitude = models.FloatField()
    longitute = models.FloatField()
    restaurant_type = models.CharField(
        max_length=2, choices=TypeChoices.choices, default=""
    )

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="ratings"
    )
    rating = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return f"Rating: {self.rating}"


class Sale(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, related_name="sales")
    income = models.DecimalField(max_digits=8, decimal_places=2)
    datetime = models.DateTimeField()

    def __str__(self) -> str:
        return f"$ {self.income}"
