from functools import partial
import itertools
from pprint import pprint
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.db.models import (
    Sum,
    Prefetch,
    Avg,
    Max,
    Min,
    Count,
    CharField,
    Value,
    F,
    Q,
    Case,
    When,
    Subquery,
    OuterRef,
    Exists,
)
from django.utils import timezone
from django.db.models.functions import Upper, Length, Concat, Coalesce
import random
from django.db import transaction

from core.forms import RatingForm, RestaurantForm, ProductOrderForm
from core.models import Restaurant, Sale, Rating, StaffRestaurant, Order


def email_user(email):
    print(f"Dear {email}, Thank you for your order")


def order_product(request: HttpRequest):
    if request.method == "POST":
        form = ProductOrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order: Order = form.save()
                order.product.number_in_stock -= order.number_of_items
                order.product.save()
                redirect("order-product")
            transaction.on_commit(partial(email_user, "phinhn@gmail.com"))
        else:
            return render(request, "order.html", {"form": form})

    form = ProductOrderForm()
    context = {"form": form}

    return render(request, "order.html", context)


def index(request: HttpRequest):

    five_days_ago = timezone.now() - timezone.timedelta(days=5)

    sales = Sale.objects.filter(restaurant=OuterRef("pk"), datetime__gte=five_days_ago)

    restaurants = Restaurant.objects.filter(Exists(sales))

    print(restaurants)

    # Filter to restaurants that have any sales with income > 85
    # restaurants = Restaurant.objects.filter(
    #     # Exists(Sale.objects.filter(restaurant=OuterRef("pk"), income__gt=85))
    #     Exists(Rating.objects.filter(restaurant=OuterRef("pk"), rating=5))
    # )
    # print(restaurants)

    # restaurants = Restaurant.objects.all()

    # # Annotate each restaurant with the income generated from its MOST RECENT sale
    # sales = Sale.objects.filter(restaurant=OuterRef("pk")).order_by("-datetime")

    # # Outer query
    # restaurants = restaurants.annotate(
    #     last_sale_income=Subquery(sales.values("income")[:1]),
    #     last_sale_expenditure=Subquery(sales.values("expenditure")[:1]),
    #     profit=F("last_sale_income") - F("last_sale_expenditure"),
    # )

    # print(restaurants)

    # restaurants = Restaurant.objects.filter(
    #     restaurant_type__in=[
    #         Restaurant.TypeChoices.ITALIAN,
    #         Restaurant.TypeChoices.CHINESE,
    #     ]
    # )

    # sales = Sale.objects.filter(restaurant__in=Subquery(restaurants.values("pk")))

    # print(len(sales))

    # sales = Sale.objects.filter(
    #     restaurant__restaurant_type__in=[
    #         Restaurant.TypeChoices.ITALIAN,
    #         Restaurant.TypeChoices.CHINESE,
    #     ]
    # )

    # print(sales.values_list("restaurant__restaurant_type", flat=True).distinct())

    # <---- Description: aggregating total Sales over each 10 days  period, starting from the first sale up until the last ---->
    # first_sale = Sale.objects.aggregate(first_sale_date=Min("datetime"))[
    #     "first_sale_date"
    # ]
    # last_sale = Sale.objects.aggregate(last_sale_date=Max("datetime"))["last_sale_date"]

    # # generate a list of dates each 10 days apart
    # dates = []
    # count = itertools.count()

    # while (dt := first_sale + timezone.timedelta(days=10 * next(count))) <= last_sale:
    #     dates.append(dt)

    # whens = [
    #     When(
    #         datetime__range=(dt, dt + timezone.timedelta(days=10)),
    #         then=Value(dt.date()),
    #     )
    #     for dt in dates
    # ]

    # case = Case(*whens, output_field=CharField())

    # sales = (
    #     Sale.objects.annotate(daterange=case)
    #     .values("daterange")
    #     .annotate(total_sales=Sum("income"))
    # )

    # print(sales)

    # restaurants = Restaurant.objects.annotate(
    #     avg_ratings=Avg("ratings__rating"), num_ratings=Count("ratings__pk")
    # )

    # print(restaurants.order_by(F("avg_ratings").desc(nulls_last=True)))

    # restaurants = restaurants.annotate(
    #     highly_rating=Case(
    #         When(avg_ratings__gt=3, num_ratings__gt=1, then=True), default=False
    #     )
    # )

    # assign a continent to each restaurant
    # type = Restaurant.TypeChoices
    # european = Q(restaurant_type__in=[type.ITALIAN, type.GREEK])
    # asian = Q(restaurant_type__in=[type.INDIAN, type.CHINESE])
    # north_american = Q(restaurant_type=type.MEXICAN)

    # restaurants = restaurants.annotate(
    #     rating_bucket=Case(
    #         When(avg_ratings__gt=3.5, then=Value("Highly Rated")),
    #         When(avg_ratings__range=(2.5, 3.5), then=Value("Average Rating")),
    #         When(avg_ratings__lt=2.5, then=Value("Bad Rating")),
    #         default=Value("None Rating"),
    #         output_field=CharField(),
    #     ),
    #     continent=Case(
    #         When(european, then=Value("Europe")),
    #         When(asian, then=Value("Asia")),
    #         When(north_american, then=Value("North America")),
    #         default=Value("Other"),
    #     ),
    # )

    # print(
    #     restaurants.values("name", "avg_ratings", "rating_bucket", "continent").filter(
    #         continent="Asia"
    #     )
    # )

    # restaurants = Restaurant.objects.annotate(number_sales=Count("sales"))

    # restaurants = restaurants.annotate(
    #     is_popular=Case(When(number_sales__gt=8, then=True), default=False)
    # )

    # italian_restaurant = Restaurant.TypeChoices.ITALIAN

    # restaurants = Restaurant.objects.annotate(
    #     is_italian=Case(
    #         When(restaurant_type=italian_restaurant, then=True), default=False
    #     )
    # )

    # restaurants = Restaurant.objects.annotate(
    #     name_value=Coalesce(F("nickname"), F("name"))
    # )

    # ratings = Rating.objects.filter(rating__lt=0).aggregate(
    #     total_rating=Coalesce(Avg("rating"), 0.0)
    # )

    # for restaurant in restaurants:
    #     for sale in restaurant.sales.all():
    #         print(sale.income)
    # We want to find all Sales where:
    #   - Profit is greate than expenditure, OR
    #   - Restaurant name contains a number

    # name_has_num = Q(restaurant__name__regex=r"[0-9]+")
    # profit_gt_expenditure = Q(income__gt=F("expenditure"))

    # sales = Sale.objects.select_related("restaurant").filter(
    #     profit_gt_expenditure, name_has_num
    # )

    # print(sales)

    # <---- Description: restaurant's name contains either the word "Italian" OR the word "Mexican" ---->
    # it_or_mx = Q(name__icontains="Italian") | Q(name__icontains="Mexican")
    # recently_opened = Q(date_opened__gt=timezone.now() - timezone.timedelta(days=50))

    # restaurants = Restaurant.objects.filter(it_or_mx, recently_opened)
    # print(restaurants)

    # Find any restaurants that have the number '1' in the name
    # restaurants = Restaurant.objects.filter(
    #     Q(name__istartswith="i") | Q(name__startswith="m")
    # )

    # Get all Italian or Mexican restaurants
    # italian_restaurant = Restaurant.TypeChoices.ITALIAN
    # mexican_restaurant = Restaurant.TypeChoices.MEXICAN
    # restaurant_types = [italian_restaurant, mexican_restaurant]

    # restaurants = (
    #     Restaurant.objects.filter(
    #         # restaurant_type__in=restaurant_types
    #         Q(restaurant_type=italian_restaurant)
    #         | Q(restaurant_type=mexican_restaurant),
    #     )
    #     # .values("name", "restaurant_type")
    # )

    # print(restaurants)

    # sales = Sale.objects.aggregate(
    #     profit=Count("id", filter=Q(income__gt=F("expenditure"))),
    #     loss=Count("id", filter=Q(income__lte=F("expenditure"))),
    # )

    # print(sales)

    # restaurants = (
    #     Restaurant.objects.all()
    #     .values("id", "name")
    #     .annotate(
    #         total_income=Sum("sales__income"),
    #         total_expenditure=Sum("sales__expenditure"),
    #         total_profit=F("total_income") - F("total_expenditure"),
    #     )
    #     .order_by("-total_profit")
    # )

    # count = restaurants.aggregate(
    #     profit_count=Count("id", filter=Q(total_income__gt=F("total_expenditure"))),
    #     loss_count=Count("id", filter=Q(total_income__lte=F("total_expenditure"))),
    # )

    # print(count)
    # print(Restaurant.objects.count( ))

    # total_profit = restaurants.annotate(
    #     total_profit=F("total_income") - F("total_expenditure")
    # ).order_by("total_profit")

    # sales = Sale.objects.select_related("restaurant").annotate(
    #     profit=F("income") - F("expenditure")
    # )
    # sales = Sale.objects.filter(expenditure__gt=F("income"))

    # for sale in sales:
    #     print(f"{sale.restaurant} Profit: {sale.profit}")

    # sales = Sale.objects.all()
    # for sale in sales:
    #     sale.expenditure = random.uniform(5, 100)
    # Sale.objects.bulk_update(sales, ["expenditure"])

    # rating = Rating.objects.first()
    # rating.rating = F("rating") + 1
    # rating.save(update_fields=["rating"])
    # rating.refresh_from_db()

    # restaurants = (
    #     Restaurant.objects.annotate(total_sales=Sum("sales__income"))
    #     # .order_by("total_sales")
    #     .filter(total_sales__gte=10)
    # )

    # print(restaurants.aggregate(avg_sales=Avg("total_sales")))

    # restaurants = Restaurant.objects.annotate(total_sales=Sum("sales__income")).values(
    #     "name", "total_sales"
    # )
    # restaurants = Restaurant.objects.values("restaurant_type").annotate(
    #     num_rating=Count("ratings"), avg_rating=Avg("ratings__rating")
    # )

    # Restaurant 1 [Rating: 4.3]
    # concatenation = Concat(
    #     "name",
    #     Value(" [Rating: "),
    #     Avg("ratings__rating"),
    #     Value("]"),
    #     output_field=CharField(),
    # )
    # restaurants = Restaurant.objects.annotate(message=concatenation)
    # for r in restaurants:
    #     print(r.message)

    # fetch all restaurants, and let's assume we want
    # to get the number of characters in the name of the restaurant. So 'xyz' == 3

    # restaurants = Restaurant.objects.annotate(
    #     len_name=Length("name"), upper_name=Upper("name")
    # ).filter(len_name__gt=10)
    # print(restaurants)

    # one_month_ago = timezone.now() - timezone.timedelta(days=31)
    # sales = Sale.objects.filter(
    #     datetime__gte=one_month_ago
    # )

    # print(
    #     sales.aggregate(
    #         max=Max("income"),
    #         min=Min("income"),
    #         cont=Count("restaurant__id"),
    #         average=Avg("income"),
    #         sum=Sum("income"),
    #     )
    # )
    # jobs = StaffRestaurant.objects.all()
    # jobs = StaffRestaurant.objects.prefetch_related("restaurant", "staff")

    # for job in jobs:
    #     print(f"{job.staff.name}-{job.restaurant.name}: {job.salary}")

    # month_ago = timezone.now() - timezone.timedelta(days=30)
    # monthly_sales = Prefetch(
    #     "sales", queryset=Sale.objects.filter(datetime__gte=month_ago)
    # )
    # # five_rating = Prefetch("ratings", queryset=Rating.objects.filter(rating__gte=5))

    # restaurants = Restaurant.objects.prefetch_related("ratings", monthly_sales).filter(
    #     ratings__rating__gte=5
    # )

    # restaurants = restaurants.annotate(total=Sum("sales__income"))

    # print(restaurants)

    # Get all 5-star ratings, and fetch all the sales for restaurants with 5-star ratings
    # restaurants = (
    #     Restaurant.objects.prefetch_related("ratings", "sales")
    #     .filter(ratings__rating=5)
    #     .annotate(total=Sum("sales__income"))
    # )
    # print(restaurants)

    # restaurants = Restaurant.objects.filter(name__istartswith="c").prefetch_related(
    #     "ratings", "sales"
    # )
    # context = {"restaurants": restaurants}

    # ratings = Rating.objects.only("rating", "restaurant__name").select_related("restaurant")
    # context = {"ratings": ratings}

    return render(request, "index.html")
    # if request.method == "POST":
    #     form = RatingForm(request.POST or None)
    #     if form.is_valid():
    #         form.save()
    #     else:
    #         return render(request, "index.html", {"form": form})
    # context = {"form": RatingForm()}
    # return render(request, "index.html", context)


def restaurant(request: HttpRequest):
    if request.method == "POST":
        form = RestaurantForm(request.POST or None)
        if form.is_valid():
            # form.save()
            print(form.cleaned_data)
        else:
            return render(request, "index.html", {"form": form})

    context = {"form": RestaurantForm()}
    return render(request, "index.html", context)
