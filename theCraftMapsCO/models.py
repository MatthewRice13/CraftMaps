from django.db import models

# Create your models here.
class Brewery_Table(models.Models):
    Brewery_ID = models.IntegerField(max_length=2000)
    Brewery_Name = models.CharField(max_length=255)
    Brewery_Town = models.CharField(max_length=255)
    Brewery_Region = models.CharField(max_length=150)
    Brewery_Latitude = models.DecimalField(max_digits=10, decimal_places=10)
    Brewery_Longitude = models.DecimalField(max_digits=10, decimal_places=10)
    Brewery_URL = models.URLField(max_length=200, null=True, blank=True)


class Beer_Table(models.Models):
    Beer_ID = models.IntegerField(max_length=2000)
    Beer_Name = models.CharField(max_length=255)
    Beer_Brewery = models.CharField(max_length=255)
    Beer_Type = models.CharField(max_length=150)
    Beer_Percent = models.DecimalField(max_digits=2, decimal_places=2)
    Beer_Rating = models.DecimalField(max_digits=2, decimal_places=2)


class Brewery_Types(models.Models):
    ID = models.IntegerField(max_length=10000)
    Brewery_ID = models.IntegerField(max_length=2000)
    Type_ID = models.IntegerField(max_length=2000)


class Types_Table(models.Models):
    Type_ID = models.IntegerField(max_length=10000)
    Type_Name = models.IntegerField(max_length=2000)