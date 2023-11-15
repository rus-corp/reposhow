from django.urls import path


from .views import (TransferMoneyToUserView,
                    PaymentCurrencyView,
                    PaymentMethodView,
                    PaymentAgregatorView,
                    # TinkofPaymentRequestView,
                    # TinkofPaymentResultView,
                    WithdrawFundsView,
                    WithdrawalEcurrencyAPIView,
                    AdvCashDepositFundsCallbackView
                    )

# from .invoice import GenerateInvoice


urlpatterns = [
    path('operation/transferuser/', TransferMoneyToUserView.as_view(), name='transfer_user'),
    path('operation/transfer/currency/', PaymentCurrencyView.as_view(), name='currency_choice'),
    path('operation/transfer/method/<str:currency>/', PaymentMethodView.as_view(), name='payment_method'),
    path('operation/transfer/agregator/<str:method>/', PaymentAgregatorView.as_view(), name='payment_agregator'),
    # path('operation/transfer/tinkof_payment/', TinkofPaymentRequestView.as_view(), name='tinkof_payment'),
    # path('operation/transfer/tinkof/request/', TinkofPaymentResultView.as_view(), name='tinkof_request'),
    path('operation/transfer/to_bank_card/request/', WithdrawFundsView.as_view(), name='send_to_band_card'),
    path('operation/transfer/to_ecurrency/request/', WithdrawalEcurrencyAPIView.as_view(), name='send_to_ecurrency'),
    path('advcash-callback/', AdvCashDepositFundsCallbackView.as_view(), name='advcash-callback'),
]