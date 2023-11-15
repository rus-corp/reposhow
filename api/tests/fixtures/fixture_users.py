import pytest


@pytest.fixture
def user(
    django_user_model,
    # EUR_acc, USD_acc,
    RUB_acc
):
    return django_user_model.objects.create(
        username="TestUser",
        email="ewrucv@ermn.ru",
        password="1234567",
        slug="werlkjdsf",
        status="FR",
        # usd_acc=USD_acc,
        # eur_acc=EUR_acc,
        rub_acc=RUB_acc,
    )


@pytest.fixture
def country():
    from app.user_docs.models import Country, Region

    region = Region.objects.create(name="Europe")
    country = Country.objects.create(name="Russia", region=region)
    return country


@pytest.fixture
def user_info(user, specialization, country):
    from app.main_users.models import UserInfo

    instance = UserInfo.objects.create(
        user=user,
        first_name="John",
        last_name="Doe",
        phone_number="555-555-5555",
        country=country,
        date_of_birth="2023-06-29",
        cost_of_hour_work=50.00,
        review_ratio=4.5,
        profile_description="This is my profile description",
        baner="path/to/baner.jpg",
    )
    instance.specialization.add(specialization)
    return instance


@pytest.fixture
def second_user(django_user_model):
    return django_user_model.objects.create(
        username="TestUser2",
        email="sdfkj@sdlfk.ru",
        password="1234567",
        slug="weroiucv",
        status="FR",
    )


@pytest.fixture
def another_user(
    django_user_model,
    USD_acc, EUR_acc, RUB_acc
):
    return django_user_model.objects.create(
        username="AnotherUser",
        email="cxvoiuwer@lkwenr.ru",
        password="123567",
        slug="xiuwer",
        status="FR",
        legal_status='PS',
        usd_acc=USD_acc,
        eur_acc=EUR_acc,
        rub_acc=RUB_acc,
    )


@pytest.fixture
def another_user_info(another_user, specialization, country):
    from app.main_users.models import UserInfo

    instance = UserInfo.objects.create(
        user=another_user,
        first_name="Joe",
        last_name="Bouie",
        phone_number="555-555-5555",
        country=country,
        date_of_birth="2023-06-29",
        cost_of_hour_work=50.00,
        review_ratio=4.5,
        profile_description="This is my profile description",
        baner="path/to/baner.jpg",
    )
    instance.specialization.add(specialization)
    return instance


@pytest.fixture
def token(client, user):
    from knox.models import AuthToken

    instance, token = AuthToken.objects.create(user=user)
    return token


@pytest.fixture
def user_client(token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    return client


@pytest.fixture
def another_token(client, another_user):
    from knox.models import AuthToken

    instance, token = AuthToken.objects.create(user=another_user)
    return token


@pytest.fixture
def another_user_client(another_token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {another_token}")
    return client
