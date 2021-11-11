from django.urls import path
from account.views import AccountView, DepositView, WithdrawView

urlpatterns = [
    path('', AccountView.as_view()),
    path('/deposit', DepositView.as_view()),
    path('/withdraw', WithdrawView.as_view())
]