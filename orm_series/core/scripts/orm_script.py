from django.contrib.auth.models import User
from django.utils import timezone
from django.db import connection
from pprint import pprint
from django.db.models.functions import Lower
import random

from core.models import Restaurant, Rating, Sale, Staff, StaffRestaurant

# Notes
# python3 manage.py runscript orm_script
# prefetch_related
# select_related


def run():
    # many-to-many: add, all, count, remove, set. clear, create, filter, exclude

    staff, created = Staff.objects.get_or_create(name="John Wick")
    staff.restaurants.clear()
    restaturants = Restaurant.objects.all()[:10]
    for restaurant in restaturants:
        staff.restaurants.add(
            restaurant, through_defaults={"salary": random.randint(20_000, 80_000)}
        )
    # staff.restaurants.set(
    #     Restaurant.objects.all()[:10],
    #     through_defaults={"salary": random.randint(20_000, 80_000)},
    # )

    # restaurant.staff_set.add(Staff.objects.get(pk=1))

    # italian_restaurants = staff.restaurants.filter(
    #     restaurant_type=Restaurant.TypeChoices.ITALIAN
    # )
    # [print(res.name) for res in italian_restaurants]
    # print(italian_restaurants.count())
    # print(staff.restaurants.all())

    # chinese = Restaurant.TypeChoices.CHINESE
    # sales = Sale.objects.filter(restaurant__restaurant_type=chinese).aaggregate(sum("income"))

    # print(sales)

    # <----- Find all ratings associated with a restaurants beginning with 'C' ------->
    # ratings = Rating.objects.filter(restaurant__name__istartswith="c")

    # for r in ratings:
    #     print(f"{r.restaurant.name}-{r.rating}")

    # <----- Filter down to only Chinese restaurants ------->
    # chinese = Restaurant.TypeChoices.CHINESE
    # indian = Restaurant.TypeChoices.INDIAN
    # mexican = Restaurant.TypeChoices.MEXICAN
    # check_types = [chinese]

    # sales = Sale.objects.filter(income__range=(50, 60))
    # # sales = restaurants.first().sales.all()
    # print([sale.income for sale in sales])

    # print(restaurant.get("name"))

    # sales = Sale.objects.first()
    # print(sales.restaurant_id)

    # restaurants = Restaurant.objects.filter(name__istartswith="i")
    # print(restaurants)

    # restaurants.update(
    #     date_opened =  timezone.now() - timezone.timedelta(days=365),
    #     website = "http://www.test.com"
    # )

    # restaurant = Restaurant.objects.first()
    # print(restaurant.name)

    # restaurant.name = "Italian Food Court"
    # restaurant.save(update_fields=["name"])

    # try:
    #     user = User.objects.first()
    #     restaurant = Restaurant.objects.first()

    #     rating = Rating(user=user, restaurant=restaurant, rating=10)

    #     rating.full_clean()
    #     rating.save()

    # except Exception as e:
    # print(e)

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
