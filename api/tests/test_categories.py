import pytest

from app.main_users.models import CustomUser


class TestCase:
    @pytest.mark.django_db(transaction=True)
    def test_category_endpoint(self, activity, category, user_client):
        response = user_client.get(f"/api/v1/activity/{activity.slug}/categories/")
        assert response.status_code == 200, (
            "Проверьте что при обращении к эндпоинту `/api/v1/activity/{activity.id}/categories/` "
            "возвращается код 200"
        )
        print(response.json())
        assert (
            response.json()[0].get("user_count")
            == CustomUser.objects.filter(
                user_info__specialization__category__slug=category.slug
            ).count()
        ), (
            "Првоерьте что поле `user_count` возвращает действительное кол-во "
            "пользователей с данной категорией"
        )

    @pytest.mark.django_db(transaction=True)
    def test_specialization_endpoint(self, specialization, category, user_client):
        response = user_client.get(
            f"/api/v1/categories/{category.slug}/specializations/"
        )
        assert response.status_code == 200, (
            "Проверьте что при обращении к эндпоинту `categories/it/specializations/` "
            "возвращается код 200"
        )
        print(response.json())
        assert (
            response.json()[0].get("user_count")
            == CustomUser.objects.filter(
                user_info__specialization__slug=specialization.slug
            ).count()
        ), (
            "Првоерьте что поле `user_count` возвращает действительное кол-во "
            "пользователей с данной категорией"
        )
