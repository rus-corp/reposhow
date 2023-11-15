from celery import shared_task
from decimal import Decimal
from django.http.response import JsonResponse
from datetime import date


from .models import Operation, Account





amount_father_rub = 500
grandfather_amount_rub = 400
grand_grandfather_amount_rub = 100

amount_father_usd = Decimal('7.5')
grandfather_amount_usd = Decimal('6')
grand_grandfather_amount_usd = Decimal('1.5')



def generate_payment_purpose(purpose, contract_number):
    purpose_map = {
        "VF": "Пополнение вступительного фонда от {}",
        "EF": "Оплата вступления в Кооператив, договор № {} без НДС",
        "DF": "Передача части вступительного взноса в Фонд развития от {}",
        "RA": "Внесение пая, договор № {} без НДС",
        "RF": "Реферальные бонусы от {}",
        "ND": "Не востребованный платеж от {}",
        "CO": "Создание заказа от {}",
        'TU': 'Перевод между юзерами от {}',
    }
    
    purpose_text = purpose_map.get(purpose, '')
    return purpose_text.format(contract_number)



def transfer_money(from_acc, to_acc, amount, currency, purpose):
    """Движение денег и создание данных об операции"""
    if from_acc.balance < amount:
        raise ValueError("Insufficient funds")
    from_acc.balance -= amount
    from_acc.save()
    
    to_acc.balance += amount
    to_acc.save()
    if purpose == 'EF' or purpose == 'VF':
        payment_purpose = generate_payment_purpose(purpose=purpose, contract_number=to_acc)
    else:
        payment_purpose = generate_payment_purpose(purpose=purpose, contract_number=from_acc)
    Operation.objects.create(
        purpose_of_payment=payment_purpose,
        currency=currency,
        value=amount,
        from_account=from_acc,
        to_account=to_acc,
    )
    
    
    
def create_order_transfer_money(customer, currency, price, order):
    user_account_mapping = {
        'RUB': customer.rub_acc,
        'USD': customer.usd_acc,
        'EUR': customer.eur_acc
    }
    order_account_mapping = {
        'RUB': order.rub_acc,
        'USD': order.usd_acc,
        'EUR': order.eur_acc
    }
    if currency in user_account_mapping:
        user_account = user_account_mapping[currency]
        order_account = order_account_mapping[currency]
        user_account.balance -= price
        order_account.balance += price
        user_account.save()
        order_account.save()
        Operation.objects.create(
            purpose_of_payment = 'CO',
            currency=currency,
            value=price,
            from_account=user_account,
            to_account = order_account
        )
    else:
        raise ValueError('invalid currency')
    
    

def check_customer_balance(customer, currency, price):
    if currency == 'RUB':
        if customer.rub_acc.balance >= price:
            return True
        else:
            return JsonResponse({'Status': False, 'message': 'Top up your balance'})
    elif currency == 'USD':
        if customer.usd_acc.balance >= price:
            return True
        else:
            return JsonResponse({'Status': False, 'message': 'Top up your balance'})
    elif currency == 'EUR':
        if customer.usd_acc.balance >= price:
            return True
        else:
            return JsonResponse({'Status': False, 'message': 'Top up your balance'})
        


def generate_account_number():
    count = Account.objects.count()
    if count > 99999999:
        raise Exception('Достигнут предел по счетам в системе')
    number = f'{date.today().strftime("%m%d")}{count:010d}'
    return number