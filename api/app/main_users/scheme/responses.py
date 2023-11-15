from drf_spectacular.utils import OpenApiResponse, OpenApiExample

from ..serializers import CustomuserResponseSerializer

example_expired = OpenApiExample(name='Bad example', status_codes=["403"], response_only=True, value={'Status': False,
                                                                                                      'Errors': 'Срок действия '
                                                                                                                'токена истек '
                                                                                                                'и он был '
                                                                                                                'удален'})
example_limit = OpenApiExample(name='Bad example 4', status_codes=["403"], response_only=True,
                               value={'Status': False, 'Errors': 'Превышен лимит проверок'})
example_token_not_found = OpenApiExample(name='Bad example 2', status_codes=["403"], response_only=True,
                                         value={'Status': False, 'Errors': 'Неверный uid или токен'})
example_no_arguments_specified = OpenApiExample(name='Bad example 4', status_codes=["403"], response_only=True,
                                                value={'Status': False,
                                                       'Errors': 'Не указаны все необходимые аргументы'})
example_easy_password = OpenApiExample(name='Bad example 3', status_codes=["403"], response_only=True,
                                       value={'Status': False,
                                              'Errors':
                                                  {'password': 'easy password'}})
example_errors = OpenApiExample(name='Bad example 4', status_codes=["403"], response_only=True,
                                value={'Status': False,
                                       'Errors':
                                           {'field': 'string'}})

resp_200 = {200: OpenApiResponse(description='Request successful.', response=CustomuserResponseSerializer(),
                                 examples=[OpenApiExample(name='Great example', status_codes=["200"],
                                                          response_only=True, value={'Status': True})])}

register_403_resp = {403: OpenApiResponse(description='Request successful.',
                                          response=CustomuserResponseSerializer(),
                                          examples=[example_easy_password,
                                                    example_no_arguments_specified,
                                                    example_errors])}

confirm_404_resp = {404: OpenApiResponse(description='Request failed.', response=CustomuserResponseSerializer(),
                                         examples=[OpenApiExample(name='Bad example', status_codes=["404"],
                                                                  response_only=True, value={'Status': False,
                                                                                             'Errors': 'Ссылка '
                                                                                                       'активации '
                                                                                                       'недействительна'
                                                                                             })])}

login_200_resp = {200: OpenApiResponse(description='Request successful.', response=CustomuserResponseSerializer(),
                                       examples=[OpenApiExample(name='Great example', status_codes=["200"],
                                                                response_only=True,
                                                                value={'Status': True, 'Token': 'string'})])}
login_403_resp = {403: OpenApiResponse(description='Request failed.', response=CustomuserResponseSerializer(),
                                       examples=[OpenApiExample(name='Bad example', status_codes=["403"],
                                                                response_only=True,
                                                                value={'Status': False,
                                                                       'Errors': 'Не удалось авторизировать.'}),
                                                 OpenApiExample(name='Bad example 2', status_codes=["403"],
                                                                response_only=True,
                                                                value={'Status': False,
                                                                       'Errors': 'Не '
                                                                                 'указаны '
                                                                                 'все '
                                                                                 'необходимые '
                                                                                 'аргументы.'})
                                                 ])}

reset_password_request_link_403_resp = {403: OpenApiResponse(description='Request failed.',
                                                             response=CustomuserResponseSerializer(),
                                                             examples=[OpenApiExample(name='Bad example',
                                                                                      status_codes=["403"],
                                                                                      response_only=True,
                                                                                      value={'Status': False,
                                                                                             'Errors': 'Данный email '
                                                                                                       'не найден'}),
                                                                       OpenApiExample(name='Bad example 2',
                                                                                      status_codes=["403"],
                                                                                      response_only=True,
                                                                                      value={'Status': False,
                                                                                             'Errors': 'Не '
                                                                                                       'указаны '
                                                                                                       'все '
                                                                                                       'необходимые '
                                                                                                       'аргументы.'})
                                                                       ])}

reset_password_link_200_resp = {200: OpenApiResponse(description='Request successful.',
                                                     response=CustomuserResponseSerializer(),
                                                     examples=[OpenApiExample(name='Great example',
                                                                              status_codes=["200"],
                                                                              response_only=True,
                                                                              value={'Status': True,
                                                                                     'uid': 'string',
                                                                                     'token': 'string'})])}
reset_password_link_403_resp = {403: OpenApiResponse(description='Request failed.',
                                                     response=CustomuserResponseSerializer(),
                                                     examples=[OpenApiExample(name='Bad example 1',
                                                                              status_codes=["404"],
                                                                              response_only=True,
                                                                              value={'Status': False,
                                                                                     'Errors':
                                                                                         'Ссылка сброса пароля '
                                                                                         'недействительна'})])}

reset_password_secure_token_403_resp = {403: OpenApiResponse(description='Request failed.',
                                                             response=CustomuserResponseSerializer(),
                                                             examples=[example_expired,
                                                                       example_token_not_found,
                                                                       example_no_arguments_specified,
                                                                       example_limit,
                                                                       ])}

reset_password_403_resp = {403: OpenApiResponse(description='Request failed.',
                                                response=CustomuserResponseSerializer(),
                                                examples=[example_expired,
                                                          example_token_not_found,
                                                          example_easy_password,
                                                          example_no_arguments_specified,
                                                          OpenApiExample(name='Bad example 5', status_codes=["403"],
                                                                         response_only=True,
                                                                         value={'Status': False,
                                                                                'Errors': 'Пароль должен быть строкой'})
                                                          ])}

account_data_403_resp = {403: OpenApiResponse(description='Request failed.',
                                              response=CustomuserResponseSerializer(),
                                              examples=[OpenApiExample(name='Bad example 1', status_codes=["403"],
                                                                       response_only=True,
                                                                       value={'Status': False,
                                                                              'Error': 'Требуется вход'}),
                                                        OpenApiExample(name='Bad example 2', status_codes=["403"],
                                                                       response_only=True,
                                                                       value={'Status': False,
                                                                              'Errors': 'Нельзя сменить адрес '
                                                                                        'электронной почты на тот же '
                                                                                        'самый'}),
                                                        example_easy_password,
                                                        example_errors
                                                        ])}
