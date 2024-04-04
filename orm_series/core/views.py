from django.shortcuts import render
from django.http import HttpRequest
from django.db.models import Sum, Prefetch, Avg, Max, Min, Count, CharField, Value
from django.utils import timezone
from django.db.models.functions import Upper, Length, Concat

from core.forms import RatingForm, RestaurantForm
from core.models import Restaurant, Sale, Rating, StaffRestaurant


# Create your views here.
def index(request: HttpRequest):

    restaurants = (
        Restaurant.objects.annotate(total_sales=Sum("sales__income"))
        # .order_by("total_sales")
        .filter(total_sales__gte=10)
    )

    print(restaurants.aggregate(avg_sales=Avg("total_sales")))

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
