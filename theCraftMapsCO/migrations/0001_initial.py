# Generated by Django 2.0.5 on 2018-08-07 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Beer_Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Beer_Name', models.CharField(max_length=155)),
                ('Beer_Brewery', models.CharField(max_length=155)),
                ('Beer_Type', models.CharField(max_length=90)),
                ('Beer_Percent', models.DecimalField(decimal_places=2, max_digits=4)),
                ('Beer_Rating', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Brewery_Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Brewery_Name', models.CharField(max_length=90)),
                ('Brewery_Region', models.CharField(default='Dublin', max_length=90)),
                ('Brewery_Address', models.CharField(default='Dublin, Ireland', max_length=500)),
                ('Brewery_Type', models.CharField(default='Brewery', max_length=50)),
                ('Brewery_Rating', models.DecimalField(decimal_places=2, default=2.5, max_digits=4)),
                ('Brewery_Latitude', models.DecimalField(decimal_places=10, max_digits=13)),
                ('Brewery_Longitude', models.DecimalField(decimal_places=10, max_digits=13)),
                ('Brewery_URL', models.URLField(blank=True, max_length=255, null=True)),
                ('Brewery_Twitter', models.URLField(blank=True, max_length=255, null=True)),
                ('Brewery_Facebook', models.URLField(blank=True, max_length=255, null=True)),
                ('Brewery_Tours', models.BooleanField(default=False)),
                ('Brewery_Merch', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User_Brewery_Ratings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Brewery_Id', models.IntegerField()),
                ('User_Id', models.IntegerField()),
                ('User_Brewery_Rating', models.DecimalField(decimal_places=2, max_digits=4)),
                ('Rating_Time_Stamp', models.DateField(blank=True)),
                ('User_Do_Tour', models.BooleanField(default=False)),
                ('User_Drink_Beer', models.BooleanField(default=False)),
                ('User_Buy_Merch', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User_Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_Favorite_Brewery_Type', models.CharField(max_length=90)),
                ('User_Max_Distance', models.IntegerField(default=20)),
                ('User_Beer_Stout', models.BooleanField(default=False)),
                ('User_Beer_Lager', models.BooleanField(default=False)),
                ('User_Beer_IPA', models.BooleanField(default=False)),
                ('User_Beer_Cider', models.BooleanField(default=False)),
                ('User_Beer_Pilsner', models.BooleanField(default=False)),
                ('User_Beer_Ale', models.BooleanField(default=False)),
                ('User_Beer_Weiss', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
