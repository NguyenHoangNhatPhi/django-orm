from django.contrib import admin
from core.models import *

# Register your models here.
sites = [Restaurant, Sale, Rating, Staff]
admin.site.register(sites)
