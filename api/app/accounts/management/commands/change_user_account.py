from django.core.management import BaseCommand
from app.main_users.models import CustomUser

class Command(BaseCommand):
    """Команда для изменение старых счетов у юзера."""

    help = 'Change user account name'

    def handle(self, *args, **kwargs):
        users = CustomUser.objects.all()
        count = 1
        for user in users:
            acc_number = f"{user.date_joined.strftime('%m%d')}"
            if not str(user.rub_acc.account_name).endswith("R"):
                user.rub_acc.account_name = f"{acc_number}{count:010d}R"
                user.rub_acc.save()
                count += 1
            if not str(user.rub_acc.account_name).endswith("U"):
                user.usd_acc.account_name = f"{acc_number}{count:010d}U"
                user.usd_acc.save()
                count += 1
            if not str(user.rub_acc.account_name).endswith("E"):
                user.eur_acc.account_name = f"{acc_number}{count:010d}E"
                user.eur_acc.save()
                count += 1