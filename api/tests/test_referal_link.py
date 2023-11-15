import pytest


class TestCase:
    @pytest.mark.django_db(transaction=True)
    def test_referal_link_get(self, client, founder_1, founder_2):
        response = client.get('/api/v1/referal-link/')
        assert response.status_code != 404, (
            "Страница `/api/v1/referal-link/` не найдена, проверьте этот адрес в *urls.py*"
        )
        assert response.status_code == 200, (
            'Првоерьте доступность эндпоинта `/api/v1/referal-link/` '
            'при обращении к нему должен возвращаться код 200'
        )
        assert 'referal_link' in response.json(), (
            'Првоерьте что при обращении к `/api/v1/referal-link/` '
            'возвращается реферальная ссылка по очереди'
        )
        referal_link = response.json()['referal_link']
        response = client.patch('/api/v1/referal-link/')
        assert response.status_code == 200, (
            'Проверьте что при PUT запросе к `/api/v1/referal-link/` '
            'возвращается код 200'
        )
        assert response.json()['referal_link'] != referal_link, (
            'Проверьте что при PUT запрсое реферальная ссылка '
            'действительн оменяет свое значение'
        )
        response = client.patch('/api/v1/referal-link/')
        assert response.status_code == 200, (
            'Проверьте что при PUT запросе к `/api/v1/referal-link/` '
            'возвращается код 200'
        )
        assert response.json()['referal_link'] == referal_link, (
            'Проверьте что при PUT запросе реферальная ссылка '
            'действительно меняет свое значение по кругу на изначальное'
        )
