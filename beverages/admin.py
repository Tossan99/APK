from django.contrib import admin
from .models import Beverage, Category

# Register your models here.
admin.site.register(Beverage)
admin.site.register(Category)