import csv
from typing import Any, Optional
import os

from django.core.management.base import BaseCommand

from app.categories.models import Activity, Category

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'categ.csv')

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(file_path, 'r') as file:
            categories = list(csv.DictReader(file, delimiter=';'))


        Category.objects.all().delete()
        for cat in categories:
            activ = Activity.objects.filter(name=cat['activity']).first()
            c = Category(name=cat['name'], activity=activ)
            c.save()