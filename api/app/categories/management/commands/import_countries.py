import csv
import os
from typing import Any, Optional
from django.core.management.base import BaseCommand


from app.user_docs.models import Country, Region

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'countr.csv')

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(file_path, 'r') as file:
            countries = list(csv.DictReader(file, delimiter=';'))
            
        for country in countries:
            reg = Region.objects.get(name=country['region_name'])
            c = Country(name=country['name'], phone_code=f"+{country['phone_code']}",flag=f"flags/{country['flag']}" ,region=reg)
            c.save()
        