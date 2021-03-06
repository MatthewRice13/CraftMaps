from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    Brewery_Tours = models.BooleanField(default=False)
    Brewery_Merch = models.BooleanField(default=False)

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


class User_Table(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    User_Favorite_Brewery_Type = models.CharField(max_length=90)
    User_Max_Distance = models.IntegerField(default=20)
    User_Beer_Stout = models.BooleanField(default=False)
    User_Beer_Lager = models.BooleanField(default=False)
    User_Beer_IPA = models.BooleanField(default=False)
    User_Beer_Cider = models.BooleanField(default=False)
    User_Beer_Pilsner = models.BooleanField(default=False)
    User_Beer_Ale = models.BooleanField(default=False)
    User_Beer_Weiss = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        User_Table.objects.create(user=instance)

class User_Brewery_Ratings(models.Model):
    Brewery_Id = models.IntegerField()
    User_Id = models.IntegerField()
    User_Brewery_Rating = models.DecimalField(max_digits=4, decimal_places=2)
    Rating_Time_Stamp = models.DateField(blank=True)
    User_Do_Tour = models.BooleanField(default=False)
    User_Drink_Beer = models.BooleanField(default=False)
    User_Buy_Merch = models.BooleanField(default=False)
