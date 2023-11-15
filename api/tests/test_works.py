import pytest

from app.portfolio.models import Work


class TestCase:
    @pytest.mark.django_db(transaction=True)
    def test_works_access(self, client, user):
        response = client.get(f"/api/v1/works/list/{user.id}/")
        assert response.status_code == 200, (
            "Првоерьте доступ к эндпоинту `/api/v1/works/list/{user.id}/` "
            "а также его наличие в файле urls.py"
        )

    @pytest.mark.django_db(transaction=True)
    def test_work_edit(self, user_client, work):
        data = {"title": "New title", "price": 2000}
        response = user_client.patch(
            f"/api/v1/works/update/{work.id}/", data=data
        )
        assert response.status_code == 200, (
            "Проверьте что при PUT запросе к `/api/v1/works/update/{work.id}/` "
            "возвращается код 200"
        )
        assert response.json().get("title") == data["title"], (
            "Проверьте что редактирование портфолио по эндпоинту `/api/v1/works/update/{work.id}/` "
            "возможно"
        )
        assert int(response.json().get("price")[:-3]) == data["price"], (
            "Проверьте что редактирование портфолио по эндпоинту `/api/v1/works/update/{work.id}/` "
            "возможно"
        )

    @pytest.mark.django_db(transaction=True)
    def test_work_create(self, user_client):
        instances = Work.objects.count()
        data = {}
        response = user_client.post("/api/v1/works/create/", data=data)
        assert response.status_code == 400, (
            "Првоерьте что при POSt запросе к `/api/v1/works/create/` "
            "в неправильнымт данными возвращается код 400"
        )
        data = {
            "title": "test_work",
            "description": "salfjwr",
            "table_place": "2"
        }
        response = user_client.post("/api/v1/works/create/", data=data)
        print(response.json())
        assert response.status_code == 201, (
            "првоерьте что при POST запросе к `/api/v1/works/create/` "
            "с валидными данными возвращается код 201"
        )
        assert instances + 1 == Work.objects.count(), (
            "Првоерьте что при создании объекта модели POST запросом",
            "он появляется в бд.",
        )
