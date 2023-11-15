from django.core.management.base import BaseCommand

from app.portfolio.models import Work, CurrentWork
from app.main_users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = CustomUser.objects.all()
        for user in users:
            works = Work.objects.filter(user=user)
            current_works = CurrentWork.objects.filter(user=user)
            
            for index, work in enumerate(works):
                work.table_place = index
                work.save()
            
            for index, current_work in enumerate(current_works):
                current_work.table_place = index
                current_work.save()
