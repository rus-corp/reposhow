import pytest

from app.orders.models import Order


class TestCase:
    @pytest.mark.django_db(transaction=True)
    def test_order_access(self, client):
        response = client.get("/api/v1/orders/")
        assert (
            response.status_code != 404
        ), "Страница `/api/v1/orders/` не найдена, проверьте этот адрес в *urls.py*"

    @pytest.mark.django_db(transaction=True)
    def test_order_not_auth(self, client):
        response = client.get("/api/v1/orders/")
        assert response.status_code == 200, (
            "Проверьте, что запросы на `/api/v1/orders/` "
            "доступны не только аутентифицированным пользователям"
        )

    @pytest.mark.django_db(transaction=True)
    def test_orders_get(self, user_client, order):
        response = user_client.get("/api/v1/orders/")
        assert response.status_code == 200, (
            "Проверьте что при GET запросе от аутентифицированного пользователя"
            " к `/api/v1/orders/` возвращается код 200"
        )
        response = user_client.get(f"/api/v1/orders/{order.slug}/")
        assert response.status_code == 200, (
            "Проверьте что при GET запросе от аутентифицированного пользователя"
            " к `/api/v1/orders/{order.slug}/` возвращается код 200"
        )
        json_data = response.json()
        assert "avatar" in json_data.get("customer")["user_info"], (
            "Проверьте что при запросе к `/api/v1/orders/{order.slug}/` "
            "возвращается фото из профиля заказчика"
        )
        assert "first_name" in json_data.get("customer")["user_info"], (
            "Проверьте что при запросе к `/api/v1/orders/{order.slug}/` "
            "возвращается имя заказчика"
        )
        assert "last_name" in json_data.get("customer")["user_info"], (
            "Проверьте что при запросе к `/api/v1/orders/{order.slug}/` "
            "возвращается фамилия заказчика"
        )
        assert "company_name" in json_data.get("customer")["user_info"], (
            "Проверьте что при запросе к `/api/v1/orders/{order.slug}/` "
            "возвращается фото из профиля заказчика"
        )

    @pytest.mark.django_db(transaction=True)
    def test_orders_create(
        self, user_client, specialization, user, country, another_user
    ):
        instances_count = Order.objects.count()

        data = {}
        response = user_client.post("/api/v1/orders/", data=data)
        assert response.status_code == 400, (
            "Проверьте что при POST запросе на создание заказа"
            "с невалидными данными возвращается код 400"
        )

        data = {
            "name": "wersdfwer",
            "description": "strsdfwersdfsdfing",
            "price": "2815",
            "currency": "RUB",
            "specialization_id": specialization.id,
            "period": "2023-10-29",
            "status": "MD",
            "country": [
                {
                    "name": country.name,
                }
            ],
        }
        response = user_client.post("/api/v1/orders/", data=data)
        assert response.status_code == 201, (
            "Првоерьте что при POST запросе на создание заказов "
            "с валидными данными возвращается код 201"
        )
        assert instances_count + 1 == Order.objects.count(), (
            "Проверьте что при POST запросе на создание заказа с "
            "валидными данными - новая запись появляется в бд"
        )
