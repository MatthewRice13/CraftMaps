from django.contrib import admin
from .models import Brewery_Table, Beer_Table

# Register your models here.
admin.site.register(Brewery_Table)
admin.site.register(Beer_Table)
