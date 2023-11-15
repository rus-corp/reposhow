import pytest


@pytest.fixture
def founder_1(django_user_model, EUR_acc, USD_acc, RUB_acc):
    return django_user_model.objects.create(
        username="TestsdfwerdwUser",
        email="ewrucsdfwersdqwv@ermn.ru",
        password="1234567",
        slug="werlqwe23kjdsf",
        referal_link='321',
        status="FR",
        founder=True,
        usd_acc=USD_acc,
        eur_acc=EUR_acc,
        rub_acc=RUB_acc,
    )


@pytest.fixture
def founder_2(django_user_model, EUR_acc, USD_acc, RUB_acc):
    return django_user_model.objects.create(
        username="TessadfwertUser",
        email="ewrusdfwercv@ermn.ru",
        password="1234567",
        slug="werlksdfwerjdsf",
        founder=True,
        referal_link='123',
        status="FR",
        usd_acc=USD_acc,
        eur_acc=EUR_acc,
        rub_acc=RUB_acc,
    )
