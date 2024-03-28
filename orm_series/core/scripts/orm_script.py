from django.contrib.auth.models import User
from django.utils import timezone
from django.db import connection
from pprint import pprint

from core.models import Restaurant, Rating, Sale


# python3 manage.py runscript orm_script


def run():
    try:
        user = User.objects.first()
        restaurant = Restaurant.objects.first()

        rating = Rating(user=user, restaurant=restaurant, rating=10)

        rating.full_clean()
        rating.save()

    except Exception as e:
        print(e)

    # rating, created = Rating.objects.get_or_create(
    #     restaurant=restaurant, user=user, rating=4
    # )

    # if created:
    #     print("The rating was created successfull.")
    # else:
    #     print("The rating has existed")

    # restaurant = Restaurant.objects.first()

    # print(restaurant.sales.all())

    # restaurant = Restaurant.objects.first()
    # user = User.objects.first()

    # Rating.objects.create(user=user, restaurant=restaurant, rating=3)

    # restaurant = Restaurant()
    # restaurant.name = "Italian Restaurant"
    # restaurant.latitude = 50.2
    # restaurant.longitute = 50.2
    # restaurant.date_opened = timezone.now()
    # restaurant.restaurant_type = Restaurant.TypeChoices.ITALIAN

    # restaurant.save()

    # Restaurant.objects.create(
    #     name="Pizza Shop",
    #     date_opened=timezone.now(),
    #     restaurant_type=Restaurant.TypeChoices.ITALIAN,
    #     latitude=50.2,
    #     longitute=50.2,
    # )
    # print("Save done")

    # pizza_shop = Restaurant.objects.filter(name="Pizza Shop").first()
    # pizza_shop.website = "https://pizzahut.vn/"
    # pizza_shop.save()

    # print(Restaurant.objects.count())
    # print(connection.queries)

    pprint(connection.queries)
