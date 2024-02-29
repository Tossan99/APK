from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    """
    A view for the home page
    """
    return render(request, 'beverages/index.html')