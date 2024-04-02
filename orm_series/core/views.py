from django.shortcuts import render
from django.http import HttpRequest
from django.db.models import Sum, Prefetch
from django.utils import timezone

from core.forms import RatingForm, RestaurantForm
from core.models import Restaurant, Sale, Rating, StaffRestaurant


# Create your views here.
def index(request: HttpRequest):
    jobs = StaffRestaurant.objects.prefetch_related("restaurant", "staff")

    for job in jobs:
        print(f"{job.staff.name}-{job.restaurant.name}: {job.salary}")

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
