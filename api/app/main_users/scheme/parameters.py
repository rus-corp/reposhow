from drf_spectacular.utils import OpenApiParameter

uid_param = OpenApiParameter(name='uidb64', type=str, location=OpenApiParameter.PATH, required=True,
                             description='Зашифрованный id пользователя (подставляется из url при нажатии '
                                         'пользователем на ссылку)')
token_param = OpenApiParameter(name='token', type=str, location=OpenApiParameter.PATH, required=True,
                               description='Токен подтверждения почты (подставляется из url при нажатии'
                                           ' пользователем на ссылку)')
