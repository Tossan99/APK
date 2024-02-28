from django.shortcuts import render
from django.http import HttpResponse

def beverages_list(request):
    return HttpResponse("Hello, Beverages!")