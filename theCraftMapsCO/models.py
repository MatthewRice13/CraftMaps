from django.db import models


# Create your models here.
class Brewery_Table(models.Model):
    Brewery_Name = models.CharField(max_length=90)
    Brewery_Region = models.CharField(max_length=90, default='Dublin')
    Brewery_Address = models.CharField(max_length=500, default='Dublin, Ireland')
    Brewery_Type = models.CharField(max_length=50, default='Brewery')
    Brewery_Rating = models.DecimalField(max_digits=4, decimal_places=2, default=2.5)
    Brewery_Latitude = models.DecimalField(max_digits=13, decimal_places=10)
    Brewery_Longitude = models.DecimalField(max_digits=13, decimal_places=10)
    Brewery_URL = models.URLField(max_length=255, null=True, blank=True)
    Brewery_Twitter = models.URLField(max_length=255, null=True, blank=True)
    Brewery_Facebook = models.URLField(max_length=255, null=True, blank=True)

    def _str_(self):
        return self.Brewery_Name


class Beer_Table(models.Model):
    Beer_Name = models.CharField(max_length=155)
    Beer_Brewery = models.CharField(max_length=155)
    Beer_Type = models.CharField(max_length=90)
    Beer_Percent = models.DecimalField(max_digits=4, decimal_places=2)
    Beer_Rating = models.DecimalField(max_digits=4, decimal_places=2)

    def _str_(self):
        return self.Beer_Name
