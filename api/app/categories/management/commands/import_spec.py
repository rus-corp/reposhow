import csv
from typing import Any, Optional
import os

from django.core.management.base import BaseCommand

from app.categories.models import Category, Specialization

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'spec.csv')

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(file_path, 'r') as file:
            specializations = list(csv.DictReader(file, delimiter=';'))

        Specialization.objects.all().delete()
        for spec in specializations:
            categ = Category.objects.filter(name=spec['category']).first()
            c = Specialization(name=spec['name'], category=categ)
            c.save()
            
            
# Логопедия;Дошкольное образование 
# Познавательно-речевое;Дошкольное образование 
# Скорочтение;Дошкольное образование 