from django.db import models


# Create your models here.
class Brewery_Table(models.Model):
    Brewery_Name = models.CharField(max_length=90)
    Brewery_Region = modesl.CharField(max_length=90)
    Brewery_Address = models.CharField(max_length=500)
    Brewery_Type = models.CharField(max_length=50, default='Brewery')
    Brewer_Rating = models.DecimalField(max_digits=2, decimal_palces=2, default=2.5)
    Brewery_Latitude = models.DecimalField(max_digits=10, decimal_places=10)
    Brewery_Longitude = models.DecimalField(max_digits=10, decimal_places=10)
    Brewery_URL = models.URLField(max_length=255, null=True, blank=True)
    Brewery_Twitter = models.URLField(max_length=255, null=True, blank=True)
    Brewery_Facebook = models.URLField(max_length=255, null=True, blank=True)

    def _str_(self):
        return self.Brewery_Name


class Beer_Table(models.Model):
    Beer_Name = models.CharField(max_length=155)
    Beer_Brewery = models.CharField(max_length=155)
    Beer_Type = models.CharField(max_length=90)
    Beer_Percent = models.DecimalField(max_digits=2, decimal_places=2)
    Beer_Rating = models.DecimalField(max_digits=2, decimal_places=2)

    def _str_(self):
        return self.Beer_Name
