from django.shortcuts import render
from .models import Category, Beverage

def beverages_list(request):
    """ A view to show all products, including sorting and search queries """
    beverages = Beverage.objects.all()
    
    context = {
        'beverages': beverages,
    }

    return render(request, 'beverages/beverages_list.html', context)