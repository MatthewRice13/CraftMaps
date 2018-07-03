from background_task import background
from .models import Brewery_Table
import data_prep


# background tasks
# python manage.py process_tasks
@background(schedule=60)
def add_brewery_data():

    data = data_prep.complete_data()
    for d in data:
        entry = Brewery_Table(
                                Brewery_Name=d['name'],
                                Brewery_Town=d['address'],
                                Brewery_Region=d['address'],
                                Brewery_Type=d['type'],
                                Brewery_Latitude=d['lati'],
                                Brewery_Longitude=d['long'],
                                Brewery_URL=d['url']
                              )
        entry.save()


@background(schedule=60)
def update_database():
    data = scrape_data()
    brewery = Brewery_Table.objects.all().count()



