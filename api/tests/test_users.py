import pytest


from app.raiting.models import Rating


class TestCase:
    @pytest.mark.django_db(transaction=True)
    def test_personal_account_output(self, user_client, user, user_info):
        response = user_client.get("/api/v1/personal-account/")
        assert response.status_code != 404, (
            "Проверьте доступ к эндпоинту `/api/v1/personal-account/` "
            "а также его наличие в urls.py"
        )
        response = user_client.get("/api/v1/personal-account/")
        # print(response.json())
        assert "time_registered" in response.json()[0]["user_info"], (
            "Провеьте что в response выводится поле time_registered при запросе к "
            "эндпоинту `/api/v1/personal-account/`"
        )
        assert (
            "rub_account" in response.json()[0]
            and response.json()[0].get("rub_account")
            == user.rub_acc.account_name
        ), (
            "Провеьте что в response выводится поле rub_account при запросе к "
            "эндпоинту `/api/v1/personal-account/`"
        )

    @pytest.mark.django_db(transaction=True)
    def test_freelancers_endpoint(selg, user_client):
        response = user_client.get("/api/v1/freelancers/")
        assert response.status_code != 404, (
            "Проверьте доступ к эндпоинту `/api/v1/freelancers/` "
            "а также его наличие в файле urls.py"
        )
        assert response.status_code == 200, (
            "Проверьте при обращении к эндпоинту `/api/v1/freelancers/` "
            "возвращается код 200"
        )

    # @pytest.mark.django_db(transaction=True)
    # def test_rating_get_endpoint(self, user_client, neg_rev_1, neg_rev_2, user):
    #     response = user_client.patch('/api/v1/rating/')
    #     assert response.status_code == 200, (
    #         "Првоерьте что при Get запросе к `/api/v1/rating/` "
    #         "возвращается код 200"
    #     )
