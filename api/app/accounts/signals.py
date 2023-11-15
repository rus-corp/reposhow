# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.db.models import Q
# from django.contrib.auth import get_user_model

# from app.mails.models import Notification
# from app.accounts.models import Account


# User = get_user_model()


# @receiver(post_save, sender=Account)
# def create_notification(sender, instance, created, **kwargs):
#     Notification.objects.create(
#         template_link='mails/Acount_deposit.html',
#         context={},
#         email=User.objects.get(
#             Q(rub_acc_id__account_name=instance.account_name) |
#             Q(usd_acc_id__account_name=instance.account_name) |
#             Q(eur_acc_id__account_name=instance.account_name)
#         ).email,
#         title='New Deposit!',
#         type_of_notifications='refill'
#     )
#     return
