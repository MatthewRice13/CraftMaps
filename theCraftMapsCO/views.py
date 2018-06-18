from django.shortcuts import render
from .models import Brewery_Table

# Create your views here.
def home(request):
    brewery = Brewery_Table.objects.all()
    context = {
        'brewery': brewery
    }
    return render(request, 'homepage.html', context)