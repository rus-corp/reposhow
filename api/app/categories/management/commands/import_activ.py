import csv
from typing import Any, Optional
import os
from django.core.management.base import BaseCommand

from app.categories.models import Activity

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'active.csv')


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(file_path, 'r') as file:
            activity = list(csv.DictReader(file, delimiter=';'))

        Activity.objects.all().delete()
        for activ in activity:
            a = Activity(name=activ['name'])
            a.save()
    
