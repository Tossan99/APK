from django.urls import path
from . import views

urlpatterns = [
    path("", views.beverages_list, name="beverages"),
]