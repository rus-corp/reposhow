import pytest

from app.chat.models import Thread, Comment, ChatRoom, Messages


class TestChatApi:
    @pytest.mark.django_db(transaction=True)
    def test_treads_canbe_opened_unauth(self, client):
        response = client.get("/api/v1/threads/")
        assert (
            response.status_code == 200
        ), "Проверьте, что на `/api/v1/threads/` при запросе без токена возвращаете статус 200"

    @pytest.mark.django_db(transaction=True)
    def test_tread_canbe_opened_unauth(self, client, thread):
        response = client.get(f"/api/v1/threads/{thread.id}/")
        assert (
            response.status_code == 200
        ), "Проверьте, что на `/api/v1/threads/{thread.id}/` при запросе без токена возвращаете статус 200"

    @pytest.mark.django_db(transaction=True)
    def test_thread_creation(self, user_client):
        threads_count = Thread.objects.count()

        data = {}
        response = user_client.post("/api/v1/threads/", data=data)
        assert response.status_code == 400, (
            "Проверьте, что при POST запросе на `/api/v1/threads/` "
            "с не правильными данными возвращается статус 400"
        )
        data = {"title": "Новое обсуждение", "text": "обсуждаем"}
        response = user_client.post("/api/v1/threads/", data=data)
        assert response.status_code == 201, (
            "Проверьте, что при POST запросе на `/api/v1/threads/` "
            "с правильными данными возвращается статус 201"
        )
        test_data = response.json()
        assert test_data.get("title") == data["title"], (
            "Проверьте, что при POST запросе на `/api/v1/threads/` возвращается"
            "словарь с данными нового треда."
        )
        assert test_data.get("text") == data["text"], (
            "Проверьте, что при POST запросе на `/api/v1/threads/` возвращается"
            "словарь с данными нового треда."
        )
        assert "created_at" in test_data, (
            "Проверьте, что при POST запросе на `/api/v1/threads/` возвращается"
            "словарь с данными нового треда."
        )
        assert threads_count + 1 == Thread.objects.count(), (
            "Проверьте, что при POST запросе `/api/v1/threads/` создается"
            "новый тред."
        )

    @pytest.mark.django_db(transaction=True)
    def test_Comment(self, client, thread):
        response = client.get(f"/api/v1/threads/{thread.id}/comments/")
        print(response.status_code)
        assert response.status_code == 200 or response.status_code != 404, (
            "Проверьте наличе эндпоинта `/api/v1/threads/{thread.id}/comments/`"
            "и что по запросу неавторизованного пользователя возвращается код 200"
        )

    @pytest.mark.django_db(transaction=True)
    def test_Comment_to_thread(self, user_client, thread):
        Comment_count = Comment.objects.count()
        data = {}
        response = user_client.get(f"/api/v1/threads/{thread.id}/comments/")
        assert response.status_code == 200, (
            "Проверьте, что при запросе на `/api/v1/threads/{thread.id}/comments/`"
            "пользователь с токеном получает код 200"
        )
        response = user_client.post(
            f"/api/v1/threads/{thread.id}/comments/", data=data
        )
        assert response.status_code != 201, (
            "Проверьте, что при POST запросе на `/api/v1/threads/{thread.id}/comments/`"
            "без входных данных коммент не создается."
        )
        data = {
            "thread": thread.id,
            "text": "Коментарий",
        }
        response = user_client.post(
            f"/api/v1/threads/{thread.id}/comments/", data=data
        )
        assert (
            response.status_code == 201
            and Comment_count + 1 == Comment.objects.count()
        ), (
            "Проверьте, что при POST запросе `/api/v1/threads/{thread.id}/comments/` с валидными данными"
            "комментарий создается."
        )
        json_data = response.json()
        assert (
            json_data.get("text") == data["text"]
        ), "Проверьте, что после создания коммента возвращается информация созданного объекта"

    @pytest.mark.django_db(transaction=True)
    def test_comment_to_comment(self, user_client, comment, thread):
        Comment_count = Comment.objects.count()
        data = {
            "text": "Комментарий",
            "comment": comment.id,
        }
        response = user_client.post(
            f"/api/v1/threads/{thread.id}/comments/", data=data
        )
        assert (
            response.status_code == 201
        ), "Проверьте, что при создании комментария на комметарий возвращается код 201"
        assert (
            Comment_count + 1 == Comment.objects.count()
        ), "Проверьте, что комментарий на комментарий может создаваться и появляться в таблице."

    @pytest.mark.django_db(transaction=True)
    def test_chat_access_detail(self, another_user_client, chat, chat_1):
        response_1 = another_user_client.get(f"/api/v1/chats/{chat.id}/")
        response_2 = another_user_client.get(f"/api/v1/chats/{chat_1.id}/")
        assert (
            response_1.json() != response_2.json()
        ), "Проверьте что при обращении к разным чатам по их айди - возвращаются разные объекты"

    @pytest.mark.django_db(transaction=True)
    def test_personal_chat(self, user_client, another_user):
        instances_count = ChatRoom.objects.count()

        data = {"user_2": another_user.id}
        response = user_client.post("/api/v1/chats/", data=data)
        assert response.status_code == 201, (
            "Проверьте, что при POST запросе к `/api/v1/chats/` "
            "с правильными данными возвращается 201"
        )
        assert instances_count + 1 == ChatRoom.objects.count(), (
            "Проверьте что при POST запросе к `/api/v1/{chat_1.id}/chat/` с валидными данными "
            "в бд появляется новая запись"
        )

    @pytest.mark.django_db(transaction=True)
    def test_chat_errors(self, user_client, chat_1, another_user):
        instances_count = ChatRoom.objects.count()

        response = user_client.post(
            "/api/v1/chats/", data={"user_2", another_user.id}
        )
        assert response.status_code == 400, (
            "Проверьте что при отправке повторного POST запроса на создание чата"
            " возвращается код 400"
        )
        assert instances_count == ChatRoom.objects.count(), (
            "Проверьте что при повторном запросе на создание комнаты"
            " в бд не создается новой модели"
        )

    @pytest.mark.django_db(transaction=True)
    def test_chat_access(self, user_client, chat):
        response = user_client.get(f"/api/v1/chats/{chat.id}/")
        assert (
            "messages" not in response.json()
        ), "Проверьте, что при GET запросе к своим чатам, пользователь не может получить доступ к чужим"

    @pytest.mark.django_db(transaction=True)
    def test_chat_get_endpoint(self, another_user_client, chat, chat_1):
        response = another_user_client.get('/api/v1/chats/')
        assert response.status_code == 200, (
            'Проверьте что при GET запросе к `/api/v1/chats/` '
            'возвращается код 200'
        )
        assert len(response.json()) == 2, (
            'Првоерьте что в ответе возвращаются все чаты пользователя.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_messages_endpoints_access(self, user_client, chat_1):
        response = user_client.get(f"/api/v1/chats/{chat_1.id}/message/")
        assert response.status_code != 404, (
            "Проверьте наличие эндпоинта `/api/v1/chats/{chat_1.id}/message/` "
            "в файле urls.py."
        )

    @pytest.mark.django_db(transaction=True)
    def test_sending_messages(self, user_client, chat_1):
        instances_count = Messages.objects.count()

        data = {}
        response = user_client.post(
            f"/api/v1/chats/{chat_1.id}/message/", data=data
        )
        assert response.status_code == 400, (
            "Проверьте что при отправке POST запроса с невалидными данными к эндпоинту "
            "`/api/v1/chats/{chat_1.id}/message/` возвращается код 400"
        )

        data = {"message": "Hi there!"}
        response = user_client.post(
            f"/api/v1/chats/{chat_1.id}/message/", data=data
        )
        assert response.status_code == 201, (
            "проверьте, что при отправке POST запрос к `/api/v1/chats/{chat_1.id}/message/` "
            "с валидными данными возвращается код 201"
        )
        assert instances_count + 1 == Messages.objects.count(), (
            "проверьте, что при отправке POST запрос к `/api/v1/chats/{chat_1.id}/message/` "
            "с валидными данными создается новый объект модели"
        )
        json_data = response.json()
        assert (
            "message" in json_data
            and json_data.get("message") == data["message"]
        ), (
            "Првоерьте что при отправке сообщения POST запросом "
            "возвращаются данные полей созданной модели"
        )
        assert (
            json_data.get("room") == chat_1.id
        ), "Проверьте, что сообщения создаются в приналежащей юзерам чат комнате"
        response = user_client.get(f"/api/v1/chats/{chat_1.id}/")
        assert (
            len(response.json().get("messages")) == 1
        ), "Проверьте что отправленные сообщения возвращаются в списке чатов пользователя."
