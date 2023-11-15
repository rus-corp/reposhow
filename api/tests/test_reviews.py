import pytest

from app.reviews.models import Review


class TestCase:
    @pytest.mark.django_db(transaction=True)
    def test_reviews_endpoint_access(self, client, user, review):
        response = client.get(f"/api/v1/reviews/list/{user.id}/")
        assert response.status_code != 404, (
            "Проверьте наличие эндпоинта `/api/v1/reviews/list/{user.id}/` "
            "в файле urls.py"
        )
        assert (
            response.status_code == 200
        ), (
            "Проверьте доступ к эндпоиту `/api/v1/reviews/list/{user.id}/` "
        )
        response = client.get(f'/api/v1/reviews/{review.id}/')
        assert response.status_code == 200, (
            'Проверьте доступ к эндпоиту `/api/v1/reviews/{review.id}/` '
            'а также его наличие в файле urls.py'
        )

    @pytest.mark.django_db(transaction=True)
    def test_reviews_create(
        self,
        another_user_client,
        another_user,
        user,
        user_client,
        order,
        second_user,
    ):
        instances = Review.objects.count()

        data = {}
        response = user_client.post(
            "/api/v1/reviews/create/", data=data
        )
        assert response.status_code == 400, (
            "Проверьте, что при отправке POST запроса к эндпоинту "
            "`/api/v1/reviews/create/` с неправильными данными возвращается"
            "код 400"
        )

        data = {
            "order": order.id,
            "description": "какое-то собщение",
            "status": "PT",
            "customer": another_user.id,
            "executor": user.id,
        }
        response = another_user_client.post(
            "/api/v1/reviews/create/", data=data
        )
        print(response.json())
        assert response.status_code == 201, (
            "Првоерьте, что при POST запросе к `/api/v1/reviews/create/` "
            "с валидными данными возвращается код 201"
        )
        assert instances + 1 == Review.objects.count(), (
            "Проверьте, что при успешном  создании объектов модели "
            "он появляется в таблице"
        )
        data = {
            "order": order.id,
            "description": "какое-то собщение",
            "status": "PT",
            "customer": another_user.id,
            "executor": second_user.id,
        }
        response = another_user_client.post(
            "/api/v1/reviews/create/", data=data
        )
        assert response.status_code != 201, (
            "Проверьте что заказчик не может создать отзыв на исполнителя "
            "который этот заказ не выполнял"
        )
        data = {
            "order": order.id,
            "description": "какое-то собщение",
            "status": "PT",
            "customer": second_user.id,
            "executor": user.id,
        }
        response = another_user_client.post(
            "/api/v1/reviews/create/", data=data
        )

        assert response.status_code != 201, (
            "Проверьте что друйго заказчик не может оставить фрилансеру "
            "отзыв по чужому заказу"
        )
