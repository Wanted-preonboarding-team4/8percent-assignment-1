from django.urls import path
from account.views import AccountView, DepositView, WithdrawView, TransationView

urlpatterns = [
    path('', AccountView.as_view()),
    path('/deposit', DepositView.as_view()),
    path('/withdraw', WithdrawView.as_view()),
    path('/transactions/<int:account_id>', TransationView.as_view()),
]