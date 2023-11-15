import pytest


@pytest.fixture
def thread(user):
    from app.chat.models import Thread

    return Thread.objects.create(
        creator=user, title="Новый тред", text="какой-то вопрос для обсуждения"
    )


@pytest.fixture
def RUB_acc():
    from app.accounts.models import Account
    from app.adv_cash.models import PaymentAgregator

    instance = Account.objects.create(
        currency="RUB", account_name="12398908sdf", balance=0
    )
    PaymentAgregator.objects.create(name='dsflkjwer', account=instance)
    return instance


@pytest.fixture
def USD_acc():
    from app.accounts.models import Account

    return Account.objects.create(
        currency="USD", account_name="12398908safsdf", balance=0
    )


@pytest.fixture
def EUR_acc():
    from app.accounts.models import Account

    return Account.objects.create(
        currency="EUR", account_name="12398sdf908sdf", balance=0
    )


@pytest.fixture
def comment(another_user, thread):
    from app.chat.models import Comment

    return Comment.objects.create(
        thread=thread, commentator=another_user, text="Комментарий"
    )


@pytest.fixture
def chat(second_user, another_user):
    from app.chat.models import ChatRoom

    return ChatRoom.objects.create(
        user_1=second_user,
        user_2=another_user,
        name="Room1",
    )


@pytest.fixture
def chat_1(user, another_user):
    from app.chat.models import ChatRoom

    return ChatRoom.objects.create(
        user_1=user,
        user_2=another_user,
        name="Room2",
    )


@pytest.fixture
def message(chat_1, second_user):
    from app.chat.models import Messages, ChatRoom

    return Messages.objects.create(
        sender=second_user, message="Hi there!", room=ChatRoom.objects.first()
    )


@pytest.fixture
def work(user):
    from app.portfolio.models import Work

    return Work.objects.create(
        user=user,
        title="Test work",
        description="This is a test work",
        table_place="2",
    )


@pytest.fixture
def activity():
    from app.categories.models import Activity

    return Activity.objects.create(name="Разработка IT", slug="razrabotka")


@pytest.fixture
def category(activity):
    from app.categories.models import Category

    return Category.objects.create(name="IT", slug="it", activity=activity)


@pytest.fixture
def specialization(category):
    from app.categories.models import Specialization

    return Specialization.objects.create(
        name="Backend", slug="backend", category=category
    )


@pytest.fixture
def order(
    specialization,
    another_user_info,
    user
):
    from app.orders.models import Order

    instance = Order.objects.create(
        name="test order",
        description="desc of order",
        price=0,
        currency="RUB",
        specialization=specialization,
        slug="test_order",
        status='PB',
        customer=another_user_info.user,
        rub_acc=another_user_info.user.rub_acc,
        eur_acc=another_user_info.user.eur_acc,
        usd_acc=another_user_info.user.usd_acc,
    )
    instance.executor.add(user)
    return instance


@pytest.fixture
def review(another_user, order, user):
    from app.reviews.models import Review

    return Review.objects.create(
        customer=another_user,
        executor=user,
        description='message to zews',
        order=order,
        status='PT'
    )


@pytest.fixture
def neg_rev_1(another_user, order, user):
    from app.reviews.models import Review

    return Review.objects.create(
        customer=another_user,
        executor=user,
        description='message to zews',
        order=order,
        status='NT'
    )


@pytest.fixture
def neg_rev_2(another_user, order, user):
    from app.reviews.models import Review

    return Review.objects.create(
        customer=another_user,
        executor=user,
        description='message to zews',
        order=order,
        status='NT'
    )
