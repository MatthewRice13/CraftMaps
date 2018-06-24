from django.db import models


# Create your models here.
class Brewery_Table(models.Model):
    Brewery_Name = models.CharField(max_length=255)
    Brewery_Town = models.CharField(max_length=255)
    Brewery_Region = models.CharField(max_length=120)
    Brewery_Type = models.CharField(max_length=120, default='Brewery')
    Brewery_Latitude = models.DecimalField(max_digits=50, decimal_places=10)
    Brewery_Longitude = models.DecimalField(max_digits=50, decimal_places=10)
    Brewery_URL = models.URLField(max_length=200, null=True, blank=True)


class Beer_Table(models.Model):
    Beer_Name = models.CharField(max_length=255)
    Beer_Brewery = models.CharField(max_length=255)
    Beer_Type = models.CharField(max_length=120)
    Beer_Percent = models.DecimalField(max_digits=2, decimal_places=2)
    Beer_Rating = models.DecimalField(max_digits=2, decimal_places=2)
